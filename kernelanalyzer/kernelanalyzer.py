import sys
import re
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
#from termcolor import colored
import os

ipmaccprefix=os.path.dirname(os.path.realpath(__file__))+"/../ipmacc/"
sys.path.extend(['.', '..', ipmaccprefix+'./pycparser/', ipmaccprefix+"/srcML/wrapper/", ipmaccprefix, ipmaccprefix+'/src/', ipmaccprefix+'/srcML/wrapper/'])
from pycparser import c_parser, c_ast
from utils_clause import clauseDecomposer,clauseDecomposer_break
from wrapper import srcml_code2xml, srcml_get_fcn_calls, srcml_get_var_details, srcml_get_parent_fcn, srcml_get_all_ids, srcml_get_declared_vars, srcml_find_var_size, srcml_get_fwdecls, srcml_prefix_functions, srcml_get_kernelargs, srcML, srcml_get_arrayaccesses

from subprocess import call, Popen, PIPE
import tempfile

from optparse import OptionParser

# Operation control
ENABLE_INDENT=False
CLEARXML=True
VERBOSE=0
ERRORDUMP=True
REDUCTION_TWOLEVELTREE=True # two-level tree reduction is the default policy.
    # setting the control to False, generates only CUDA code which is supported on limited number of devices (cc>=1.3). 
USEPYCPARSER=False # True: pycparser, False: srcML
WARNING=False 

# Debugging level control
DEBUG=0 #general
DEBUGCP=0 #copy statement
DEBUGCPARSER=0 #parsers
DEBUGVAR=False #variable type/size/name tracking
DEBUGLD=False   # loop detector
DEBUGPRIVRED=False #private/reduction statements
DEBUGSTMBRK=False
DEBUGFC=False #function call
DEBUGSRCML=False   #debugging srcml 
DEBUGSRCMLC=False #debugging srcml wrapper calls
DEBUGFWDCL=False #debug forward declaration and function redeclaration
DEBUGITER=False
DEBUGCPP=False #debug cpp call
DEBUGSMC=False

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

class codegen(object):
    def __init__(self, target, foname, nvcc_args):
        self.oacc_kernelId=0     # number of kernels which are replaced by function calls
        self.oacc_kernels=[]     # array of kernels' roots (each element of array is ElementTree)
        self.oacc_kernelsParent=[]   # array of functions name, indicating which function is the parent of kernel (associated with each elemnt in self.oacc_kernels)
        self.oacc_kernelsVarNams=[] # list of array of variables defined in the kernels' call scope
        self.oacc_kernelsVarTyps=[] # list of array of type of variables defined in the kernels' call scope
        self.oacc_kernelsLoopIteratorsPar=[]   # list of array of iterators of independent/parallel loops
        self.oacc_kernelsLoopIteratorsSeq=[]   # list of array of iterators of sequential loop
        self.oacc_kernelsAutomaPtrs=[]  # per kernel list of variables defined as deviceptr in the respective kernels or data region (no action)
        self.oacc_kernelsManualPtrs=[]  # per kernel list of variables defined explicitly to be copied in, copied out, or allocated in the respective kernels or data region 
        self.oacc_kernelsImplicit=[] # implicit copies corresponding to this kernel
        self.oacc_kernelsReductions=[] # per kernel list of variable to be reduced (used for copy-in copy-out)
        self.oacc_kernelsPrivatizin=[] # per kernel list of variable to be privated (used for copy-in copy-out)
        self.oacc_kernelsTemplates=[] # templates corresponding to each kernel
        self.oacc_kernelsAssociatedCopyIds=[] # a list of oacc_copys identifiers associated with each kernel
        self.oacc_loopSMC=[] # per call list of variables to be cached in SMC
        self.oacc_loopReductions=[] # per call list of variable to be reduced 
        self.oacc_loopPrivatizin=[] # per call list of variable to be privated 
        self.oacc_scopeAutomaPtr='' # carry the variables which are deviceptrs across the current data (not kernels) region scope
        self.oacc_scopeManualPtr='' # carry the variables which are declared explicitly for copy or allocate in current data (not kernels) region scope

        self.oacc_copyId=0  # number of copys which are replaced by function calls
        self.oacc_copys=[]  # array of copys' expression (each element is string)
        self.oacc_copysParent=[]   # array of functions name, indicating the function which is the parent of copy (associated with each elemnt in self.oacc_copys)
        self.oacc_copysVarNams=[] # list of array of variables defined in the copys' call scope
        self.oacc_copysVarTyps=[] # list of array of type of variables defined in the copys' call scope
        
        self.code='' # intermediate generated C code
        self.code_include='#include <stdlib.h>\n#include <stdio.h>\n#include <assert.h>\n#include <openacc.h>\n' # .h code including variable decleration and function prototypes
        #self.code_include='#include <stdlib.h>\n#include <stdio.h>\n#include <assert.h>\n#include <openacc.h>\nvoid ipmacc_prompt(char *s){\nif (getenv("IPMACC_VERBOSE"))\nprintf("%s",s);\n}\n' # .h code including variable decleration and function prototypes
        self.code_include+='#define IPMACC_MAX1(A)   (A)\n'
        self.code_include+='#define IPMACC_MAX2(A,B) (A>B?A:B)\n'
        self.code_include+='#define IPMACC_MAX3(A,B,C) (A>B?(A>C?A:(B>C?B:C)):(B>C?C:B))\n'
        self.active_types=[] # list of types which have at least one variable in the region scope
                             # keep track of types used in this code to forward declare undeclared types
        self.active_types_decl=[] # list of tuple (type name, type forward declaration, and full declaration)
                             # declaration of active types which are not standard
        self.active_calls=[] # list of types which have at least one variable in the region scope
                             # keep track of calls used in this code to declare them
        self.active_calls_decl=[] # list of tuple (call name, and call forward declaration)
                             # declaration of active calls which are not standard
        self.intrinsic_calls_ocl= [ 'acos', 'acosh', 'acospi', 'asin', 'asinh', 'asinpi', 'atan', 'atan2', 'atanh', 'atanpi', 'atan2pi',
                                'cbrt', 'ceil', 'copysign', 'cos', 'cosh', 'cospi', 'erfc', 'erf', 'exp', 'exp2', 'exp10', 'expm1',
                                'fabs', 'fdim', 'floor', 'fma', 'fmax', 'fmin', 'fmod', 'fract', 'frexp', 'hypot', 'ilogb', 'ldexp',
                                'lgamma', 'lgamma_r', 'log', 'log2', 'log10', 'log1p', 'logb', 'mad', 'maxmag', 'minmag', 'modf',
                                'nan', 'nextafter', 'pow', 'pown', 'powr', 'remainder', 'remquo', 'rint', 'rootn', 'round', 'rsqrt',
                                'sin', 'sincos', 'sinh', 'sinpi', 'sqrt', 'tan', 'tanh', 'tanpi', 'tgamma', 'trunc', 'half_cos',
                                'half_divide', 'half_exp', 'half_exp2', 'half_exp10', 'half_log', 'half_log2', 'half_log10', 'half_powr',
                                'half_recip', 'half_rsqrt', 'half_sin', 'half_tan', 'native_cos', 'native_divide', 'native_exp', 'native_exp',
                                'native_exp2', 'native_exp10', 'native_log', 'native_log2', 'native_log10', 'native_powr', 'native_recip',
                                'native_rsqrt', 'native_sin', 'native_sqrt',
                                'abs', 'abs_diff', 'add_sat', 'hadd', 'rhadd', 'clamp', 'clz', 'mad_hi', 'mad_sat', 'max', 'min', 
                                'mul_hi', 'rotate', 'sub_sat', 'upsample', 'mad24', 'mul24',
                                'clamp', 'degrees', 'max', 'min', 'radians', 'step', 'smoothstep', 'sign', 'cross', 'dot', 'distance', 'length', 
                                'normalize', 'fast_distance', 'fast_normalize', 'isequal', 'isnotequal', 'isgreater', 'isgreaterequal', 
                                'isless', 'islessequal', 'islessgreater', 'isfinite', 'isinf', 'isnan', 'isnormal', 'isordered', 'isunordered',
                                'signbit', 'any', 'all', 'bitselect', 
                                'vloadn', 'vstoren', 'vload_half', 'vload_halfn',
                                'vstore_half', 'vstore_half_rte', 'vstore_half_rtz', 'vstore_half_rtn', 'vstore_half_rtp', 
                                'vstore_halfn', 'vstore_halfn_rte', 'vstore_halfn_rtz', 'vstore_halfn_rtn', 'vstore_halfn_rtp', 
                                'prefetch' ]
                                # opencl calls which are available within kernel
        self.intrinsic_calls_cuda= [ 'rsqrtf', 'rsqrtf', 'sqrtf', 'cbrtf', 'rcbrtf', 'hypotf', 'expf', 'exp2f', 'exp10f', 'expm1f', 
                                'logf', 'log2f', 'log10f', 'log1pf', 'sinf', 'cosf', 'tanf', 'sincosf', 'sinpif', 'cospif', 
                                'asinf', 'acosf', 'atanf', 'atan2f', 'sinhf', 'coshf', 'tanhf', 'asinhf', 'acoshf', 'atanhf', 
                                'powf', 'erff', 'erfcf', 'erfinvf', 'erfcinvf', 'erfcxf', 'lgammaf', 'tgammaf', 'fmaf', 'frexpf', 
                                'ldexpf', 'scalbnf', 'scalblnf', 'logbf', 'ilogbf', 'j0f', 'j1f', 'jnf', 'y0f', 'y1f', 
                                'ynf', 'fmodf', 'remainderf', 'remquof', 'modff', 'fdimf', 'truncf', 'roundf', 'rintf', 'nearbyintf', 
                                'ceilf', 'floorf', 'lrintf', 'lroundf', 'llrintf', 'llroundf', 'sqrt', 'rsqrt', 'cbrt', 'rcbrt', 
                                'hypot', 'exp', 'exp2', 'exp10', 'expm1', 'log', 'log2', 'log10', 'log1p', 'sin', 
                                'cos', 'tan', 'sincos', 'sinpi', 'cospi', 'asin', 'acos', 'atan', 'atan2', 'sinh', 
                                'cosh', 'tanh', 'asinh', 'acosh', 'atanh', 'pow', 'erf', 'erfc', 'erfinv', 'erfcinv', 
                                'erfcx', 'lgamma', 'tgamma', 'fma', 'frexp', 'ldexp', 'scalbn', 'scalbln', 'logb', 'ilogb', 
                                'j0', 'j1', 'jn', 'y0', 'y1', 'yn', 'fmod', 'remainder', 'remquo', 'modf', 
                                'fdim', 'trunc', 'round', 'rint', 'nearbyint', 'ceil', 'floor', 'lrint', 'lround', 'llrint', 
                                'llround', 'x/y', 'sinf', 'cosf', 'tanf', 'sincosf', 'logf', 'log2f', 'log10f', 'expf', 
                                'exp10f', 'powf', '__fadd_', '__fmul_', '__fmaf_', '__frcp_', '__fsqrt_', '__fdiv_', '__fdividef', '__expf', 
                                '__exp10f', '__logf', '__log2f', '__log10f', '__sinf', '__cosf', '__sincosf', '__tanf', '__sinf', '__powf', 
                                'exp2f', '__dadd_', '__dmul_', '__fma_', '__ddiv_', '__drcp_', '__dsqrt_']
                                # cuda calls which are available in the kernel
        self.intrinsic_types_cuda= [ 'char1', 'uchar1', 'char2', 
                                'uchar2', 'char3', 'uchar3', 'char4', 'uchar4', 'short1', 'ushort1', 'short2', 'ushort2', 'uint2', 
                                'int3', 'uint3', 'int4', 'uint4', 'long1', 'ulong1', 'short3', 'ushort3', 'short4', 'ushort4', 
                                'int1', 'uint1', 'int2', 'long2', 'ulong2', 'long3', 'ulong3', 'long4', 'ulong4', 'longlong1', 
                                'ulonglong1', 'longlong2', 'ulonglong2', 'float1', 'float2', 'float3', 'float4',
                                'double1', 'double2', 'double3', 'double4']
                                # cuda types which are available

        self.code_kernels=[] # list of code generated for kernels
        self.nvcc_args=nvcc_args

        # variable mapper
        self.varmapper=[]   # tuple of (function_name, host_variable_name, device_variable_name)
        self.varmapper_allocated=[]
        self.prefix_varmapper = '__autogen_device_'
        self.suffix_present = '_prstn'

        # constants
        self.prefix_kernel='__ungenerated_kernel_region_'
        self.prefix_kernel_gen='__generated_kernel_region_'
        self.prefix_datacp='__ungenerated_data_copy_'
        self.prefix_datacpin='__ungenerated_data_copyin_'
        self.prefix_datacpout='__ungenerated_data_copyout_'
        self.prefix_dataalloc='__ungenerated_data_alloc_'
        self.prefix_dataimpli='__ungenerated_implicit_data'
        self.prefix_kernel_uid='__kernel_getuid'
        self.prefix_kernel_reduction_shmem='__kernel_reduction_shmem_'
        self.prefix_kernel_reduction_region='__kernel_reduction_region_'
        self.prefix_kernel_privred_region='__kernel_privred_region_'
        self.prefix_kernel_smc_fetch='__kernel_smc_fetch_' # it may encompass fetch/initilization for one or more arrays
        self.prefix_kernel_smc_fetchend='__kernel_smc_fetchend_' # it may encompass fetch/initilization for one or more arrays
        self.prefix_kernel_smc_varpref='__kernel_smc_var_data_' 
        self.prefix_kernel_smc_tagpref='__kernel_smc_var_tag_' 
        self.prefix_kernel_reduction_iterator='__kernel_reduction_iterator'
        self.prefix_kernel_reduction_lock='__ipmacc_reduction_lock_'
        self.prefix_kernel_reduction_array='__ipmacc_reduction_array_'
        #self.blockDim='256'
        self.blockDim_cuda='256'
        self.blockDim_opencl='256'

        # ast tree
        self.astRoot=0
        self.astRootML=0
    
        # codegeneration control
        if (target=='nvcuda'):
            self.target_platform = 'CUDA'
        else:
            self.target_platform = 'OPENCL' # alternatives are 'CUDA' 'OPENCL'

        # cuda carriers
        self.cuda_kernelproto=''
        self.cuda_kerneldecl =''

        # output file
        self.foname = foname

    # auxilary functions
    # - replace 1 from the end of string
    def replace_last(self, source_string, replace_what, replace_with):
        head, sep, tail = source_string.rpartition(replace_what)
        return head + replace_with + tail

    def acc_detected(self):
        return len(self.oacc_kernels)>0
    
    def wrapFuncName(self, fname):
        return fname.replace(',','_')

    def print_loopAttr(self,root):
        str ='Loop attribute> '
        str+='independent="'+root.attrib.get('independent')+'" '
        str+='private="'+root.attrib.get('private')+'" '
        str+='reduction="'+root.attrib.get('reduction')+'" '
        str+='gang="'+root.attrib.get('gang')+'" '
        str+='vector="'+root.attrib.get('vector')+'" '
        str+='smc="'+root.attrib.get('smc')+'" '
        str+='terminate="'+root.attrib.get('terminate')+'" '
        str+='init="'+root.attrib.get('init')+'" '
        str+='incoperator="'+root.attrib.get('incoperator')+'" '
#        str+='dimloops="'+root.attrib.get('dimloops')+'" '
        print str

    def unique_priv_list(self, privred):
        unq_list=[]
        for [priredV, priredI, priredO, corr, typ] in privred:
            unq=True
            for [UpriredV, UpriredI, UpriredO, Ucorr, Utyp] in unq_list:
                if (priredV==UpriredV and priredI==UpriredI and priredO==UpriredO and corr==Ucorr and typ==Utyp):
                    unq=False
                    break
            if unq:
                unq_list.append([priredV, priredI, priredO, corr, typ])
        return unq_list
        
    #
    #
    # forward declaration
    def clear_type(self, tp):
        return ' '.join(tp.replace('*','').strip().split())
    def iskeyword(self, id):
        keywords=[  'for', 'if', 'while',
                'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum', 'extern',
                'float', 'for', 'goto', 'if', 'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static',
                'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while'
                'inline', '_Bool', '_Complex', '_Imaginary',
                '__FUNCTION__', '__PRETTY_FUNCTION__', '__alignof', '__alignof__', '__asm',
                '__asm__', '__attribute', '__attribute__', '__builtin_offsetof', '__builtin_va_arg',
                '__complex', '__complex__', '__const __extension__', '__func__', '__imag', '__imag__',
                '__inline', '__inline__', '__label__', '__null', '__real', '__real__',
                '__restrict', '__restrict__', '__signed', '__signed__', '__thread', '__typeof',
                '__volatile', '__volatile__',
                'restric']
        try:
            idx=keywords.index(id)
        except:
            return False
        return True
    def builtin_type(self, tp):
        #tp=self.clear_type(tp)
        types =['signed char', 'unsigned char', 'char', 'short int', 'unsigned short int', 'int', 'unsigned int', 'long int', 'unsigned long int', 'long long int', 'unsigned long long int']
        types+=['float', 'double', 'long double', 'float _Complex']
        types+=['double _Complex', 'long double _Complex']
        types+=['__complex__ float', '__complex__ double', '__complex__ long double', '__complex__ int']
        types+=['long long unsigned int', 'bool']
        try:
            idx=types.index(tp)
        except:
            return False
        return True
    def forward_declare_append_new_types(self, listOfType):
        self.active_types+=listOfType
        self.active_types=list(set(self.active_types))

    def forward_declare_dumps_types(self):
        for i in self.active_types:
            print 'declared type: "'+i+'"'

    def implant_function_prototypes(self):
        if self.target_platform=='CUDA':
            self.code=srcml_prefix_functions(self.code, self.oacc_kernelsParent)
        elif self.target_platform=='OPENCL':
            nop=True
        else:
            print 'error: unimplemented platform'

    def forward_declare_find(self):
        # find the declaration of the undeclared calls/types listed in self.active_calls and self.active_types
        # the declaration will be stored in self.active_calls_decl and self.active_types_decl for future uses
        # 1) determine the list of undeclared types
        undecls_types=[]
        codein=self.preprocess_by_gnu_cpp(self.code)
        for i in self.active_types:
            tp=self.clear_type(i)
            if not self.builtin_type(tp):
                undecls_types.append(tp)
        undecls_types=list(set(undecls_types))
        # 2) determine the list undeclared function calls
        undecls_calls=[]
        for i in self.active_calls:
            if i.find('__kernel_privred_region_')==-1 and i.find('__kernel_reduction_region_')==-1:
                undecls_calls.append(i)
        undecls_calls=list(set(undecls_calls))
        # 3) debugging
        if DEBUGFWDCL:
            print 'looking for declaration of following types: "'+'" "'.join(undecls_types)+'"'
            print 'looking for declaration of following calls: "'+'" "'.join(undecls_calls)+'"'
        # 4) find the declaration
        [self.active_types_decl, self.active_calls_decl]=srcml_get_fwdecls(codein, undecls_types, undecls_calls, self.intrinsic_calls_ocl)
        # 5) debugging
        if DEBUGFWDCL:
            decls=self.active_types_decl
            for i in range(0,len(decls)):
                [type, fw_decl, full_decl, ocl_full_decl]=decls[i]
                print '===== forward declarations '+str(i)+': type<'+type+'> fwdecl<'+fw_decl+'> fulldecl<'+full_decl+'> oclfulldecl<'+ocl_full_decl+'>'
            decls=self.active_calls_decl
            for i in range(0,len(decls)):
                [call, proto, body]=decls[i]
                print '===== forward declarations '+str(i)+': call<'+call+'> prototype<'+proto+'> fulldecl<'+body+'>'

    #
    # dump final openacc-equivalent function calls (data copies, kernels, ...)
    #
    def oacc_copyWb(self,id,expression):
        fhandle=open(self.prefix_datacp+str(id)+'.xml','w')
        fhandle.write(expression)
        fhandle.close()

    def code_kernelDump(self,id):
        if len(self.oacc_kernels)<id:
            print 'kernel '+str(id)+'not available'
        else:
            #self.oacc_kernels[id].getroottree().write('dummy.xml')
            old_stdout = sys.stdout
            sys.stdout = open(self.prefix_kernel+str(id)+'.xml','w')
            ET.dump(self.oacc_kernels[id])
            sys.stdout = old_stdout
    
    def code_kernelPrint(self,id):
        if len(self.oacc_kernels)<id:
            print 'kernel '+str(id)+'not available'
        else:
            self.code_kernelDescendentPrint(self.oacc_kernels[id],0)

    def code_kernelDescendentPrint(self, root, depth):
        if root.getchildren()==[]:
            print str(root.text)
        else:
            print bcolors.WARNING+str(' '*depth)+str(root.tag)+str(root.attrib)+bcolors.ENDC
            for child in root:
                self.code_kernelDescendentPrint(child,depth+1)

    def util_copyIdAppend(self, expressionIn, expressionAlloc, expressionOut, depth, expressionAll):
        #if expressionIn!='':
        #    self.code=self.code+('\t'*depth)+self.prefix_dataalloc+str(self.oacc_copyId)+'();'
        #    self.code=self.code+('\t'*depth)+self.prefix_datacp+str(self.oacc_copyId)+'();'
        #    self.oacc_copys.append([self.oacc_kernelId,expressionIn])
        #    self.oacc_copyId=self.oacc_copyId+1
        ##   - create (allocation)
        #if expressionAlloc!='':
        #    self.code=self.code+('\t'*depth)+self.prefix_dataalloc+str(self.oacc_copyId)+'();'
        #    self.code=self.code+('\t'*depth)+self.prefix_datacp+str(self.oacc_copyId)+'();'
        #    self.oacc_copys.append([self.oacc_kernelId,expressionAlloc])
        #    self.oacc_copyId=self.oacc_copyId+1
        ##   - copy, copyout (allocation)
        #if expressionOut!='':
        #    self.code=self.code+('\t'*depth)+self.prefix_dataalloc+str(self.oacc_copyId)+'();'
        #    copyoutId=self.oacc_copyId
        #    self.oacc_copys.append([self.oacc_kernelId,expressionOut])
        #    self.oacc_copyId=self.oacc_copyId+1
        if expressionAll=='':
            return -1
        else:
            self.code=self.code+('\t'*depth)+self.prefix_dataalloc+str(self.oacc_copyId)+'();'
            self.code=self.code+('\t'*depth)+self.prefix_datacpin+str(self.oacc_copyId)+'();'
            copyoutId=self.oacc_copyId
            self.oacc_copyId=self.oacc_copyId+1
            self.oacc_copys.append([self.oacc_kernelId,expressionAll])
            return copyoutId

    def oacc_data_dynamicAllowed(self, clause):
        clauses=['present', 'deviceptr']
        for c in clauses:
            if c==clause:
                return True
        return False

    def oacc_data_clauseparser(self,clause,type,inout,present,dID):
        # parse openacc data clause and return correponding type (copyin, copyout, copy, pcopyin, pcopyout, pcopy)
        code=''
        regex = re.compile(r'([A-Za-z0-9_]+)([\ ]*)(\((.+?)\))*')
        #regex = re.compile(r'([A-Za-z0-9_]+)([\ ]*)(\((.+?)\))*')
        #regex = re.compile(r'([A-Za-z0-9\ ]+)\((.+?)\)')
        #for i in regex.findall(clause):
        for [i0, i3] in clauseDecomposer_break(clause):
            if DEBUGVAR:
                print 'name-input pair: '+i0+'-'+i3
            if str(i0).strip()==type:
                for j in str(i3).split(','):
                    #tcode=tcode+'<copy '
                    tcode=''
                    # varname
                    tcode=tcode+'varname="'+str(j).replace(' ','').split('[')[0]+'" '
                    # in/out
                    tcode=tcode+'in="'+inout+'" '
                    #tcode=tcode+'in="'+('true' if inout=='in' else 'false')+'" '
                    # present
                    tcode=tcode+'present="'+present+'" '
                    # dimensions
                    regex2 = re.compile(r'\[(.+?)\]')
                    dims=regex2.findall(str(j).replace(' ',''))
                    for dim in range(0,len(dims)):
                        tcode=tcode+'dim'+str(dim)+'="'+dims[dim]+'" '
                    tcode+='clause="'+type+'" '
                    tcode+='dataid="'+dID+'" '
                    # end tag
                    #tcode=tcode+'></copy>\n'
                    #tcode=tcode+'\n'
                    code=code+tcode+'\n'
        return code

    def varname_extractor(self,statement):
        vname=[]
        regex=re.compile(r'(varname=")([A-Za-z0-9_]*)(")')
        for i in regex.findall(statement):
            #print i[1]
            vname.append(i[1])
        return ' '.join(vname)
            
    def oacc_clauseparser_data(self, clauses, dID):
        expressionIn=''
        expressionAlloc=''
        expressionOut=''
        expressionAll=''
        # copy-in
        for it in ['copyin', 'copy']:
            expressionIn=expressionIn+self.oacc_data_clauseparser(clauses,it,'true','false', dID)
        for it in ['pcopy', 'present_or_copy', 'pcopyin', 'present_or_copyin']:
            expressionIn=expressionIn+self.oacc_data_clauseparser(clauses,it,'true','true', dID)
        # allocate-only
        for it in ['create']:
            expressionAlloc=expressionAlloc+self.oacc_data_clauseparser(clauses,it,'create','true', dID)
        # copy-out
        for it in ['copyout', 'copy']:
            expressionOut=expressionOut+self.oacc_data_clauseparser(clauses,it,'false','false', dID)
        for it in ['pcopy', 'present_or_copy', 'pcopyout', 'present_or_copyout']:
            expressionOut=expressionOut+self.oacc_data_clauseparser(clauses,it,'false','true', dID)
        for it in ['copy', 'pcopy', 'present_or_copy', 'copyout', 'pcopyout', 'present_or_copyout', 'copyin', 'pcopyin', 'present_or_copyin', 'create', 'present', 'present_or_create']:
            expressionAll=expressionAll+self.oacc_data_clauseparser(clauses,it,'false','false',dID)
        return [expressionIn, expressionAlloc, expressionOut, expressionAll]

    def oacc_clauseparser_data_ispresent(self, clause):
        for it in ['pcopy', 'present_or_copy', 'copyout', 'pcopyout', 'present_or_copyout', 'pcopyin', 'present_or_copyin', 'present', 'present_or_create']:
            if clause==it:
                return True
        return False


    def oacc_clauseparser_flags(self,clause,type):
        # parse openacc clause and return if type exists
        code=''
        regex = re.compile(r'([A-Za-z0-9]+)([\ ]*)(\((.+?)\))*')
        #regex = re.compile(r'([A-Za-z0-9\ ]+)\((.+?)\)')
        #for i in regex.findall(clause):
        for [i0, i1] in clauseDecomposer_break(clause):
            if str(i0).strip()==type:
                return True
        return False

    def oacc_clauseparser_deviceptr(self,clause):
        # parse openacc clause and return '\n' delimited list of deviceptr variables, if exists
        code=''
        regex = re.compile(r'([A-Za-z0-9]+)([\ ]*)(\((.+?)\))*')
        #regex = re.compile(r'([A-Za-z0-9\ ]+)\((.+?)\)')
        #for i in regex.findall(clause):
        for [i0, i3] in clauseDecomposer_break(clause):
            if str(i0).strip()=='deviceptr':
                try:
                    return i3.strip().replace(',',' ')
                except:
                    print 'error: expecting argument (list of variables) for the `deviceptr` caluse'
                    exit(-1)
        return ''
    def oacc_clauseparser_if(self,clause):
        # parse openacc `if` and return condition 
        code=''
        regex = re.compile(r'([A-Za-z0-9]+)([\ ]*)(\((.+?)\))*')
        #regex = re.compile(r'([A-Za-z0-9\ ]+)\((.+?)\)')
        #for i in regex.findall(clause):
        for [i0, i3] in clauseDecomposer_break(clause):
            if str(i0).strip()=='if':
                try:
                    return i3.strip()
                except:
                    print 'error: expecting argument (condition) for the `if` caluse'
                    exit(-1)
        return ''

    # target platform code generators
    def codegen_includeHeaders(self):
        if self.target_platform=='CUDA':
            return self.includeHeaders_cuda()
        elif self.target_platform=='OPENCL':
            return self.includeHeaders_opencl()
        else:
            print 'error: unimplemented platform'
            exit(-1)
    def codegen_syncDevice(self):
        if self.target_platform=='CUDA':
            return self.syncDevice_cuda()
        elif self.target_platform=='OPENCL':
            return self.syncDevice_opencl()
        else:
            print 'error: unimplemented platform'
            exit(-1)
    def codegen_openCondition(self,cond):
        if self.target_platform=='CUDA':
            return self.openCondition_cuda(cond)
        elif self.target_platform=='OPENCL':
            return self.openCondition_opencl(cond)
        else:
            print 'error: unimplemented platform'
            exit(-1)
    def codegen_closeCondition(self,cond):
        if self.target_platform=='CUDA':
            return self.closeCondition_cuda(cond)
        elif self.target_platform=='OPENCL':
            return self.closeCondition_opencl(cond)
        else:
            print 'error: unimplemented platform'
            exit(-1)
    def codegen_reduceVariable(self, var, type, op, ctasize):
        if self.target_platform=='CUDA':
            return self.reduceVariable_cuda(var, type, op, ctasize)
        elif self.target_platform=='OPENCL':
            return self.reduceVariable_opencl(var, type, op, ctasize)
        else:
            print 'error: unimplemented platform'
            exit(-1)
    def codegen_constructKernel(self, args, decl, kernelB, kernelId, privinfo, reduinfo, ctasize, forDims, smcinfo):
        if self.target_platform=='CUDA':
            return self.constructKernel_cuda(args, decl, kernelB, kernelId, privinfo, reduinfo, ctasize, forDims, self.oacc_kernelsTemplates[kernelId], smcinfo)
        elif self.target_platform=='OPENCL':
            return self.constructKernel_opencl(args, decl, kernelB, kernelId, privinfo, reduinfo, ctasize, forDims, self.oacc_kernelsTemplates[kernelId], smcinfo)
        else:
            print 'error: unimplemented platform'
            exit(-1)
    def codegen_appendKernelToCode(self, kerPro, kerDec, kerId, forDims, args, smcinfo):
        if self.target_platform=='CUDA':
            self.appendKernelToCode_cuda(kerPro, kerDec, kerId, forDims, args)
        elif self.target_platform=='OPENCL':
            self.appendKernelToCode_opencl(kerPro, kerDec, kerId, forDims, args, smcinfo)
        else:
            print 'error: unimplemented platform'
            exit(-1)
    def codegen_memAlloc(self, dvar, size, hvar, type, scalar_copy, ispresent):
# OLD IMPLEMENTATION:
#       code=''
#        if self.target_platform=='CUDA':
#            code+=self.memAlloc_cuda(dvar, size)
#        elif self.target_platform=='OPENCL':
#            code+=self.memAlloc_opencl(dvar, size)
#        else:
#            print 'error: unimplemented platform'
#            exit(-1)
#        code+='openacc_ipmacc_insert((unsigned long long int)'+('&' if scalar_copy else '')+hvar+',(unsigned long long int)'+dvar+','+size+');\n'
# API-based IMPLEMENTATION FIXME
        if scalar_copy:
            amp='&'
            ast='*'
        else:
            amp=''
            ast=''
        if ispresent:
            fcall='acc_present_or_create' 
        else:
            fcall='acc_create'
        if self.target_platform=='CUDA':
            # TODO code=dvar+'=('+type+ast+')'+fcall+'((void*)'+amp+hvar+','+size+');\n'
            code=fcall+'((void*)'+amp+hvar+','+size+');\n'
        elif self.target_platform=='OPENCL':
            # TODO code=dvar+'=(cl_mem)'+fcall+'((void*)'+amp+hvar+','+size+');\n'
            code=fcall+'((void*)'+amp+hvar+','+size+');\n'
        else:
            print 'error: unimplemented platform'
            exit(-1)
        return code

    def codegen_accDevicePtr(self, dvar, size, hvar, type, scalar_copy):
        code=''
        if self.target_platform=='CUDA':
            code+=dvar+'=('+type+')acc_deviceptr((void*)'+('&'if scalar_copy else '')+hvar+');\n'
        elif self.target_platform=='OPENCL':
            code+=dvar+'=(cl_mem)acc_deviceptr((void*)'+('&'if scalar_copy else '')+hvar+');\n'
        else:
            print 'error: unimplemented platform'
            exit(-1)
        return code

    def codegen_accCopyin(self, host, dev, bytes, type, present, scalar_copy):
        ast=('*' if scalar_copy else '')
        code=''
        if self.target_platform=='CUDA':
            # TODO code+=dev+'=('+type+ast+')acc_'+present+'copyin((void*)'+host+','+bytes+');\n'
            code+='acc_'+present+'copyin((void*)'+host+','+bytes+');\n'
        elif self.target_platform=='OPENCL':
            # code+=dev+'=(cl_mem)acc_'+present+'copyin((void*)'+host+','+bytes+');\n'
            code+='acc_'+present+'copyin((void*)'+host+','+bytes+');\n'
        else:
            print 'error: unimplemented platform'
            exit(-1)
        return code

    def codegen_accPresent(self, host, dev, bytes, type):
        code=''
        if self.target_platform=='CUDA':
            # TODO code+=dev+'=('+type+')acc_present((void*)'+host+');\n'
            code+='acc_present((void*)'+host+');\n'
        elif self.target_platform=='OPENCL':
            # TODO code+=dev+'=(cl_mem)acc_present((void*)'+host+');\n'
            code+='acc_present((void*)'+host+');\n'
        else:
            print 'error: unimplemented platform'
            exit(-1)
        return code

    def codegen_accPCopyout(self, host, dev, bytes, type, scalar_copy):
        ast=('*' if scalar_copy else '')
        code=''
        if self.target_platform=='CUDA' or self.target_platform=='OPENCL':
            code+='acc_copyout_and_keep((void*)'+host+','+bytes+');\n'
        else:
            print 'error: unimplemented platform'
            exit(-1)
        return code
 
    def codegen_memCpy(self, des, src, size, type):
        if self.target_platform=='CUDA':
            return self.memCpy_cuda(des, src, size, type)
        elif self.target_platform=='OPENCL':
            return self.memCpy_opencl(des, src, size, type)
        else:
            print 'error: unimplemented platform'
            exit(-1)
    def codegen_devPtrDeclare(self, type, name, sccopy):
        # sccopy stands for scalar explicit copy
        if self.target_platform=='CUDA':
            return self.devPtrDeclare_cuda(type, name, sccopy)
        elif self.target_platform=='OPENCL':
            return self.devPtrDeclare_opencl(type, name, sccopy)
        else:
            print 'error: unimplemented platform'
            exit(-1)
    def codegen_getFuncDecls(self):
        # return prototype/declarations
        if self.target_platform=='CUDA':
            return self.getFuncDecls_cuda()
        elif self.target_platform=='OPENCL':
            return self.getFuncDecls_opencl()
        else:
            print 'error: unimplemented platform'
            exit(-1)
    def codegen_getTypeFwrDecl(self):
        # return prototype/declarations
        if self.target_platform=='CUDA':
            return self.getTypeFwrDecl_cuda()
        elif self.target_platform=='OPENCL':
            return self.getTypeFwrDecl_opencl()
        else:
            print 'error: unimplemented platform'
            exit(-1)
    def codegen_getFuncProto(self):
        # return prototype/declarations
        if self.target_platform=='CUDA':
            return self.getFuncProto_cuda()
        elif self.target_platform=='OPENCL':
            return self.getFuncProto_opencl()
        else:
            print 'error: unimplemented platform'
            exit(-1)
    def codegen_renameStadardTypes(self):
        # replace the types which are conflicting with cuda built-in types
        if self.target_platform=='CUDA':
            for tp in self.intrinsic_types_cuda:
                self.code = re.sub('\\b'+tp+'\\b','__ipmacc_'+tp, self.code)
        elif self.target_platform=='OPENCL':
            nop=True
        else:
            print 'error: unimplemented platform'
            exit(-1)

    # cuda platform
    def includeHeaders_cuda(self):
        self.code_include+='#include <cuda.h>\n'
    def initDevice_cuda(self):
        return ''
    def syncDevice_cuda(self):
        code=''
        code+='if (getenv("IPMACC_VERBOSE")) printf("IPMACC: Synchronizing the region with host\\n");\n'
        code+='cudaDeviceSynchronize();\n'
        return code
    def openCondition_cuda(self,cond):
        return 'if('+cond+'){\n'
    def closeCondition_cuda(self,cond):
        return '}\n'
    def appendKernelToCode_cuda(self, kerPro, kerDec, kerId, forDims, args):
        #cleanKerDec=''
        #for [tp,incstm] in self.code_getAssignments(self.var_parseForYacc(self.code+'\n'+kerDec),['fcn']):
        #    #if incstm.strip()[0:10]=='__global__':
        #    if incstm.strip().find('__global__')!=-1:
        #        cleanKerDec=incstm
        #        break
        #if cleanKerDec=='':
        #    print 'Fatal internal error! enable to retrieve back the kernel!'
        #    exit(-1)
        #print '==============================================\n'+kerDec+'==========================================\n'
        #print '==============================================\n'+self.code+'==========================================\n'
        #exit(-1)
        self.code=self.code.replace(' __ipmacc_prototypes_kernels_'+str(kerId)+' ',' '+self.codegen_getFuncProto()+kerPro+' \n')
        #self.cuda_kernelproto+=kerPro
        self.cuda_kerneldecl +=kerDec
        #self.code=kerPro+self.code+kerDec
        blockDim=self.blockDim_cuda
        #gridDim='('+'*'.join(forDims)+')/256+1'
        gridDim='('+forDims+')/'+blockDim+'+1'
        callArgs=[]
        for i in args:
            argName=i.split(' ')
            argType=' '.join(argName[0:len(argName)-1])
            argName=argName[len(argName)-1]
            if argName.find('__ipmacc_scalar')!=-1:
                argName='&'+argName.replace('__ipmacc_scalar','')
            if argName.find('__ipmacc_reductionarray_internal')!=-1:
                argName=self.prefix_kernel_reduction_array+argName
            argName=argName.replace('__ipmacc_reductionarray_internal','')
            #TODO callArgs.append(self.varmapper_getDeviceName(self.oacc_kernelsParent[kerId], argName, self.oacc_kernelsAssociatedCopyIds[kerId]))
            if argName.find('__ipmacc_deviceptr')==-1:
                callArgs.append( ('\n('+argType+')acc_deviceptr((void*)'+argName+')') if argType.find('*')!=-1 else '\n'+argName)
            else:
                argName=argName.replace('__ipmacc_deviceptr','')
                callArgs.append( '\n'+argName)
        kernelInvoc='\n/* kernel call statement '+str(self.oacc_kernelsAssociatedCopyIds[kerId])+'*/\n'
        kernelInvoc+=('if (getenv("IPMACC_VERBOSE")) printf("IPMACC: Launching kernel '+str(kerId)+' > gridDim: %d\\tblockDim: %d\\n",'+gridDim+','+blockDim+');\n')
        kernelInvoc+=self.prefix_kernel_gen+str(kerId)+'<<<'+gridDim+','+blockDim+'>>>('+(','.join(callArgs))+');'
        kernelInvoc+='\n/* kernel call statement*/\n'
        self.code=self.code.replace(self.prefix_kernel+str(kerId)+'();',kernelInvoc)
    def reduceVariable_cuda(self, var, type, op, ctasize):
        arrname=self.prefix_kernel_reduction_shmem+type
        iterator=self.prefix_kernel_reduction_iterator
        code ='\n/* reduction on '+var+' */\n'
        code+='__syncthreads();\n'
        code+=arrname+'[threadIdx.x]='+var+';\n';
        code+='__syncthreads();\n'

        # ALTERED BEGIN
        # ALTER 1 
        #code+='for('+iterator+'='+ctasize+'; '+iterator+'>1; '+iterator+'='+iterator+'/2){\n'
        #code+='if(threadIdx.x<'+iterator+' && threadIdx.x>='+iterator+'/2){\n'
        #des=arrname+'[threadIdx.x-('+iterator+'/2)]'
        #src=arrname+'[threadIdx.x]'
        #if op=='min':
        #    code+=des+'=('+(des+'>'+src)+'?'+(src)+':'+(des)+');\n'
        #elif op=='max':
        #    code+=des+'=('+(des+'>'+src)+'?'+(des)+':'+(src)+');\n'
        #else:
        #    code+=des+'='+des+op+src+';\n'
        #code+='}\n'
        #code+='__syncthreads();\n'
        #code+='}\n'
        # ALTER 2 
        code+='for('+iterator+'=blockDim.x/2;'+iterator+'>0; '+iterator+'>>=1) {\n'
        code+='if(threadIdx.x<'+iterator+'){\n'
        src=arrname+'[threadIdx.x+'+iterator+']'
        des=arrname+'[threadIdx.x]'
        if op=='min':
            code+=des+'=('+(des+'>'+src)+'?'+(src)+':'+(des)+');\n'
        elif op=='max':
            code+=des+'=('+(des+'>'+src)+'?'+(des)+':'+(src)+');\n'
        else:
            code+=des+'='+des+op+src+';\n'
        code+='}\n'
        code+='__syncthreads();\n'
        code+='}\n'
        # END OF ALTER

        code+='}// the end of '+var+' scope\n'
        # this reduction works for most devices, but can be implemented efficienctly considering device specific atomic operations
        #code+='/*atomicAdd('+var+','+var+'[0]+'+arrname+'[0]);\n\n*/'
        code+='if(threadIdx.x==0){\n'
        if REDUCTION_TWOLEVELTREE:
            code+=var+'__ipmacc_reductionarray_internal[blockIdx.x]='+arrname+'[0];\n'
        else:
            self.code_include+='__device__ unsigned long long int '+self.prefix_kernel_reduction_lock+var+'=0u;\n'
            code+='while (atomicCAS(&'+self.prefix_kernel_reduction_lock+var+', 0u, 1u)==1u){\n'
            code+='};\n'
            code+='//start global critical secion\n'
            des=var+'[0]'
            src=arrname+'[0]'
            if op=='min':
                code+=des+'=('+(des+'>'+src)+'?'+(src)+':'+(des)+');\n'
            elif op=='max':
                code+=des+'=('+(des+'>'+src)+'?'+(des)+':'+(src)+');\n'
            else:
                code+=des+'='+des+op+src+';\n'
            code+=self.prefix_kernel_reduction_lock+var+'=0u;\n'
            code+='//^D end global critical secion\n'
        code+='}\n'
        return code
    def constructKernel_cuda(self, args, decl, kernelB, kernelId, privinfo, reduinfo, ctasize, forDims, template, smcinfo):
        code=template+' __global__ void '+self.prefix_kernel_gen+str(kernelId)
        code=code+'('+(','.join(args)).replace('__ipmacc_deviceptr','')+')'
        proto=code+';\n'
        code+='{\n'
        code+='int '+self.prefix_kernel_uid+'=threadIdx.x+blockIdx.x*blockDim.x;\n'
        # fetch __ipmacc_scalar into register
        for sc in args:
            if sc.find('__ipmacc_scalar')!=-1:
                vname=sc.split(' ')[-1]
                type=sc.replace(vname,'').replace('*','')
                code+=type+' '+vname.replace('__ipmacc_scalar','')+' = '+vname+'[0];\n'
        #code+='if('+self.prefix_kernel_uid+'>='+forDims+'){\nreturn;\n}\n'
        if len(reduinfo+privinfo)>0:
            # 1) serve privates
            pfreelist=[]
            for [v, i, o, a, t] in privinfo:
                fcall=self.prefix_kernel_privred_region+str(a)+'();'
                scp=('{ //start of reduction region for '+v+' \n') if o!='U' else ''
                kernelB=kernelB.replace(fcall,scp+t+' '+v+'='+i+';\n'+fcall)
                pfreelist.append(a)
            for ids in pfreelist:
                fcall=self.prefix_kernel_privred_region+str(ids)+'();'
                kernelB=kernelB.replace(fcall,'');
            # 2) serve reductions
            decl+='int '+self.prefix_kernel_reduction_iterator+'=0;\n'
            types=[] # types to reserve space for fast shared-memory reductions
            rfreelist=[] #remove reduction calls
            reduinfo.reverse()
            for [v, i, o, a, t] in reduinfo:
                fcall=self.prefix_kernel_reduction_region+str(a)+'();'
                # 2) 1) append proper reduction code for this variable
                kernelB=kernelB.replace(fcall,self.codegen_reduceVariable(v,t,o,ctasize)+fcall)
                types.append(t)
                rfreelist.append(a)
                decl+=t+' '+v+';'
            reduinfo.reverse()
            # 2) 2) allocate shared memory reduction array
            types=list(set(types))
            for t in types:
                code=code+'__shared__ '+t+' '+self.prefix_kernel_reduction_shmem+t+'['+ctasize+'];\n'
            rfreelist=list(set(rfreelist))
            # 2) 3) free remaining fcalls
            for ids in rfreelist:
                fcall=self.prefix_kernel_reduction_region+str(ids)+'();'
                kernelB=kernelB.replace(fcall,'')

        smc_select_calls=''
        smc_write_calls=''
        if len(smcinfo)>0:
            pfreelist=[]
            for [v, t, st, p, dw, up, div, a, dimlo, dimhi] in smcinfo:
                fcall=self.prefix_kernel_smc_fetch+str(a)+'();'
                if kernelB.find(fcall)==-1:
                    # this smc does not belong to this kernel, ignore 
                    continue
                length=self.blockDim_cuda+'+'+dw+'+'+up
                # declare local memories
                decl+='\n/* declare the shared memory of '+v+' */\n'
                decl+='__shared__ '+t.replace('*','')+' '+self.prefix_kernel_smc_varpref+v+'['+length+'];\n'
                decl+='__shared__ unsigned char '+self.prefix_kernel_smc_tagpref+v+'['+length+'];\n'
                decl+='{\n'
                decl+='int iterator_of_smc=0;\n'
                decl+='for(iterator_of_smc=threadIdx.x; iterator_of_smc<('+length+'); iterator_of_smc+=blockDim.x){\n'
                decl+=self.prefix_kernel_smc_varpref+v+'[iterator_of_smc]=0;\n'
                decl+=self.prefix_kernel_smc_tagpref+v+'[iterator_of_smc]=0;\n'
                decl+='}\n__syncthreads();\n'
                decl+='}\n'
                if st=='READ_ONLY' or st=='READ_WRITE':
                    # fetch data to local memory
                    datafetch ='{ // fetch begins\nint kk;\n'
                    datafetch+='__syncthreads();\n'
                    datafetch+='for(int kk=threadIdx.x; kk<('+length+'); kk+=blockDim.x)\n'
                    datafetch+='{\n'
                    datafetch+='int idx=blockIdx.x*'+self.blockDim_cuda+'+kk-'+dw+'+'+p+';\n'
                    datafetch+='if(idx<('+dimhi+') && idx>=('+dimlo+'))\n'
                    datafetch+='{\n'
                    datafetch+=self.prefix_kernel_smc_varpref+v+'[kk]='+v+'[idx];\n'
                    datafetch+=self.prefix_kernel_smc_tagpref+v+'[kk]=1;\n'
                    datafetch+='}\n'
                    datafetch+='}\n'
                    datafetch+='__syncthreads();\n'
                    datafetch+='} // end of fetch\n'
                    datafetch+='#define '+v+'(index) __smc_select_'+str(a)+'_'+v+'(index, (blockIdx.x*'+self.blockDim_cuda+')-('+dw+'), ((blockIdx.x+1)*'+self.blockDim_cuda+')+('+up+'), '+v+', '+self.prefix_kernel_smc_varpref+v+', '+self.blockDim_cuda+', '+p+', '+dw+')\n'
                    kernelB=kernelB.replace(fcall,datafetch+'\n'+fcall)
                # construct the smc_select_ per array for READ
                smc_select_calls+='__device__ '+t.replace('*','')+' __smc_select_'+str(a)+'_'+v+'(int index, int down, int up, '+t+' g_array, '+t+' s_array, int vector_size, int pivot, int before){\n'
                if div=='false':
                    smc_select_calls+='// the pragmas are well-set. do not check the boundaries.\n'
                    smc_select_calls+='return s_array[index-(vector_size*blockIdx.x)+before-pivot];\n'
                else:
                    smc_select_calls+='// The tile is not well covered by the pivot, dw-range, and up-range\n'
                    smc_select_calls+='// dynamic runtime performs the check\n'
                    smc_select_calls+='bool a=index>=down;\n'
                    smc_select_calls+='bool b=index<up;\n'
                    smc_select_calls+='bool d=a&b;\n'
                    smc_select_calls+='if(d){\n'
                    smc_select_calls+='return s_array[index-(vector_size*blockIdx.x)+before-pivot];\n'
                    smc_select_calls+='}\n'
                    smc_select_calls+='return g_array[index];\n'
                smc_select_calls+='}\n'
                # construct the smc_write_ per array for WRITE
                smc_write_calls+='__device__ void __smc_write_'+str(a)+'_'+v+'(int index, int down, int up, '+t+' g_array, '+t+' s_array, int vector_size, int pivot, int before,'+t.replace('*','')+' value){\n'
                if div=='false':
                    smc_write_calls+='// the pragmas are well-set. do not check the boundaries.\n'
                    smc_write_calls+='s_array[index-(vector_size*blockIdx.x)+before-pivot]=value;\n'
                else:
                    smc_write_calls+='// The tile is not well covered by the pivot, dw-range, and up-range\n'
                    smc_write_calls+='// dynamic runtime performs the check\n'
                    smc_write_calls+='bool a=index>=down;\n'
                    smc_write_calls+='bool b=index<up;\n'
                    smc_write_calls+='bool d=a&b;\n'
                    smc_write_calls+='if(d){\n'
                    smc_write_calls+='s_array[index-(vector_size*blockIdx.x)+before-pivot]=value;\n'
                    smc_write_calls+='}\n'
                    smc_write_calls+='g_array[index]=value;\n'
                smc_write_calls+='}\n'
                # replace array-ref [] with function call ()
                fcallst=self.prefix_kernel_smc_fetch+str(a)+'();'
                fcallen=self.prefix_kernel_smc_fetchend+str(a)+'();'
                changeRangeIdx_start=kernelB.find(fcallst)
                changeRangeIdx_end=kernelB.find(fcallen)
                #print kernelB[changeRangeIdx_start:changeRangeIdx_end]
                if (changeRangeIdx_start==-1 ) or (changeRangeIdx_end==-1) or (changeRangeIdx_start>changeRangeIdx_end):
                    print 'fatal error! could not determine the smc range for '+v
                    exit(-1)
                # for each arrayReference of 'v', replace [] with ()
                writeIdxList=[]
                for arrayRef in re.finditer('\\b'+v+'[\\ \\t\\n\\r]*\[',kernelB[changeRangeIdx_start:changeRangeIdx_end]):
                    #skip to the end of variable
                    arrayRef_it=changeRangeIdx_start+arrayRef.start(0)
                    arrayRef_pcnt=0
                    done=False
                    while not done:
                        if kernelB[arrayRef_it]=='[':
                            #if arrayRef_pcnt==0:
                                #kernelB[arrayRef_it]='('
                                #kernelB=kernelB[:arrayRef_it]+'('+kernelB[arrayRef_it+1:]
                            arrayRef_pcnt+=1
                        elif kernelB[arrayRef_it]==']':
                            arrayRef_pcnt-=1
                            if arrayRef_pcnt==0:
                                #kernelB[arrayRef_it]=')'
                                #kernelB=kernelB[:arrayRef_it]+')'+kernelB[arrayRef_it+1:]
                                done=True
                        arrayRef_it+=1
                    # check whether it is a write access
                    iswrite=False
                    assignmentIdx=-1
                    assignmentOpr='='
                    while True:
                        if kernelB[arrayRef_it]==';':
                            break
                        elif kernelB[arrayRef_it]=='=' and kernelB[arrayRef_it+1]!='=' and (kernelB[arrayRef_it-1]==' ' or kernelB[arrayRef_it-1]=='\t' or kernelB[arrayRef_it-1]=='\n' or kernelB[arrayRef_it-1]=='+' or kernelB[arrayRef_it-1]=='|' or kernelB[arrayRef_it-1]=='&' or kernelB[arrayRef_it-1]=='-' or kernelB[arrayRef_it-1]=='\\' or kernelB[arrayRef_it-1]=='*' or kernelB[arrayRef_it-1]=='^' or kernelB[arrayRef_it-1]=='%' or kernelB[arrayRef_it-1].isalpha() or kernelB[arrayRef_it-1].isdigit()):
                            iswrite=True
                            assignmentIdx=arrayRef_it
                            if not (kernelB[arrayRef_it-1].isalpha() or kernelB[arrayRef_it-1].isdigit()):
                                assignmentOpr=(kernelB[arrayRef_it-1]+'=').strip()
                        arrayRef_it+=1
                    # keep the track of write accesses 
                    if iswrite and (st=='WRITE_ONLY' or st=='READ_WRITE'):
                        writeIdx_str=changeRangeIdx_start+arrayRef.start(0)
                        writeIdx_end=arrayRef_it+1
                        writeIdx_loc=']'.join('['.join(kernelB[writeIdx_str:assignmentIdx].split('[')[1:]).split(']')[:-1])
                        writeIdx_val=kernelB[assignmentIdx+1:writeIdx_end]
                        #writeIdx_replacer='__smc_write_'+str(a)+'_'+v+'('+v+','+self.prefix_kernel_smc_varpref+v+','+writeIdx_loc+','+writeIdx_val[:-1]+');'
                        writeIdx_replacer='__syncthreads();\n__smc_write_'+str(a)+'_'+v+'('+writeIdx_loc+', (blockIdx.x*'+self.blockDim_cuda+')-('+dw+'), ((blockIdx.x+1)*'+self.blockDim_cuda+')+('+up+'), '+v+', '+self.prefix_kernel_smc_varpref+v+', '+self.blockDim_cuda+', '+p+', '+dw+','+writeIdx_val[:-1]+');\n'
                        writeIdx_replacer+='__syncthreads();\n'
                        writeIdxList.append([v, a, p, dw, up, writeIdx_str, writeIdx_end, assignmentIdx])
                        print 'smc: write-access on ->\n\tlocation:'+writeIdx_loc+'\n\tstart-in-kernelB:'+str(writeIdx_str)+'\n\tend-in-kernelB:'+str(writeIdx_end)+'\n\tvalue-in-kernelB:'+writeIdx_val+'\n\tend-to-end-statement:<<'+kernelB[writeIdx_str:writeIdx_end]+'>> \n\treplacer:'+writeIdx_replacer
                        #kernelB[changeRangeIdx_start+arrayRef.start(0):assignmentIdx]+')('+kernelB[assignmentIdx+1:arrayRef_it]+')'
                    if (st=='READ_ONLY' or st=='READ_WRITE') and not iswrite:
                        #replace [ and ] with ( and )
                        arrayRef_it=changeRangeIdx_start+arrayRef.start(0)
                        arrayRef_pcnt=0
                        done=False
                        while not done:
                            if kernelB[arrayRef_it]=='[':
                                if arrayRef_pcnt==0:
                                    #kernelB[arrayRef_it]='('
                                    kernelB=kernelB[:arrayRef_it]+'('+kernelB[arrayRef_it+1:]
                                arrayRef_pcnt+=1
                            elif kernelB[arrayRef_it]==']':
                                arrayRef_pcnt-=1
                                if arrayRef_pcnt==0:
                                    #kernelB[arrayRef_it]=')'
                                    kernelB=kernelB[:arrayRef_it]+')'+kernelB[arrayRef_it+1:]
                                    done=True
                            arrayRef_it+=1
                # unpack and replace write-accesses
                for wi in range(len(writeIdxList)-1,-1,-1):
                    [v, a, p, dw, up, wst, wen, asgidx]=writeIdxList[wi]
                    writeIdx_loc=']'.join('['.join(kernelB[wst:asgidx].split('[')[1:]).split(']')[:-1])
                    writeIdx_val=kernelB[asgidx+1:wen]
                    writeIdx_replacer='__syncthreads();\n__smc_write_'+str(a)+'_'+v+'('+writeIdx_loc+', (blockIdx.x*'+self.blockDim_cuda+')-('+dw+'), ((blockIdx.x+1)*'+self.blockDim_cuda+')+('+up+'), '+v+', '+self.prefix_kernel_smc_varpref+v+', '+self.blockDim_cuda+', '+p+', '+dw+','+writeIdx_val[:-1]+');\n'
                    writeIdx_replacer+='__syncthreads();\n'
                    kernelB=kernelB[0:wst]+writeIdx_replacer+kernelB[wen+1:]
                # generate writeback code
                writeback=''
                if st=='READ_WRITE' or st=='WRITE_ONLY':
                    # fetch data to local memory
                    writeback ='{ // writeback begins\nint kk;\n'
                    writeback+='__syncthreads();\n'
                    writeback+='for(int kk=threadIdx.x; kk<('+length+'); kk+=blockDim.x)\n'
                    writeback+='{\n'
                    writeback+='int idx=blockIdx.x*'+self.blockDim_cuda+'+kk-'+dw+'+'+p+';\n'
                    writeback+='if(idx<('+dimhi+') && idx>=('+dimlo+'))\n'
                    writeback+='{\n'
                    writeback+=v+'[idx]='+self.prefix_kernel_smc_varpref+v+'[kk];\n'
                    writeback+='}\n'
                    writeback+='}\n'
                    writeback+='__syncthreads();\n'
                    writeback+='} // end of writeback\n' 
                    kernelB=kernelB.replace(fcallen,writeback+'\n'+fcallen)
                # undef function call ()
                if st=='READ_ONLY' or st=='READ_WRITE':
                    kernelB=kernelB.replace(fcallen,'#undef '+v+'\n'+fcallen)
                pfreelist.append(a)
            for ids in pfreelist:
                fcallst=self.prefix_kernel_smc_fetch+str(ids)+'();'
                fcallen=self.prefix_kernel_smc_fetchend+str(ids)+'();'
                kernelB=kernelB.replace(fcallst,'')
                kernelB=kernelB.replace(fcallen,'')
            ## 2) serve reductions
            #types=[] # types to reserve space for fast shared-memory reductions
            #rfreelist=[] #remove reduction calls
            #reduinfo.reverse()
            #for [v, i, o, a, t] in reduinfo:
            #    fcall=self.prefix_kernel_reduction_region+str(a)+'();'
            #    # 2) 1) append proper reduction code for this variable
            #    kernelB=kernelB.replace(fcall,self.codegen_reduceVariable(v,t,o,ctasize)+fcall)
            #    types.append(t)
            #    rfreelist.append(a)
            #    decl+=t+' '+v+';'
            #reduinfo.reverse()
            ## 2) 2) allocate shared memory reduction array
            #types=list(set(types))
            #for t in types:
            #    code=code+'__shared__ '+t+' '+self.prefix_kernel_reduction_shmem+t+'['+ctasize+'];\n'
            #rfreelist=list(set(rfreelist))
            ## 2) 3) free remaining fcalls
            #for ids in rfreelist:
            #    fcall=self.prefix_kernel_reduction_region+str(ids)+'();'
            #    kernelB=kernelB.replace(fcall,'')
        code='\n'.join([smc_select_calls,smc_write_calls])+code
        code+=decl
        code+=kernelB
        code=code+'}\n'
        for [fname, prototype, declbody] in self.active_calls_decl:
            code=re.sub('\\b'+fname+'[\\ \\t\\n\\r]*\(','__accelerator_'+fname+'(', code)
        return [proto, code]
    def memAlloc_cuda(self, var, size):
        codeM='cudaMalloc((void**)&'+var+','+size+');\n'
        return codeM
    def memCpy_cuda(self, des, src, size, type):
        codeC='cudaMemcpy('+des+','+src+','+size+','+('cudaMemcpyHostToDevice' if type=='in' else 'cudaMemcpyDeviceToHost')+');\n'
        return codeC
    def devPtrDeclare_cuda(self, type, name, sccopy):
        return type+('* ' if sccopy else ' ')+name+';\n'
    def getTypeFwrDecl_cuda(self):
        type_decls=''
        for [nm, fwdcl, fudcl, oclfudcl] in self.active_types_decl:
            type_decls+=fwdcl+'\n'
        return type_decls
    def getFuncDecls_cuda(self):
        code=''
        for [fname, prototype, declbody] in self.active_calls_decl:
            code +='__device__ '+declbody+'\n'
        for [fname, prototype, declbody] in self.active_calls_decl:
            code=re.sub('\\b'+fname+'[\\ \\t\\n\\r]*\(','__accelerator_'+fname+'(', code)
        return code
    def getFuncProto_cuda(self):
        code=''
        for [fname, prototype, declbody] in self.active_calls_decl:
            code +='__device__ '+prototype+'\n'
        for [fname, prototype, declbody] in self.active_calls_decl:
            code=re.sub('\\b'+fname+'[\\ \\t\\n\\r]*\(','__accelerator_'+fname+'(', code)
        return code

    # opencl platform
    def includeHeaders_opencl(self):
        self.code_include+='#include <CL/cl.h>\n'
        self.code_include+=self.initDeviceVar_opencl()
    def initDeviceVar_opencl(self):
        codeC=''
        codeC+='extern cl_int __ipmacc_clerr ;\n'
        codeC+='extern cl_context __ipmacc_clctx ;\n'
        codeC+='extern size_t __ipmacc_parmsz;\n'
        codeC+='extern cl_device_id* __ipmacc_cldevs;\n'
        codeC+='extern cl_command_queue __ipmacc_command_queue;\n'
        return codeC
    def syncDevice_opencl(self):
        code=''
        code+='if (getenv("IPMACC_VERBOSE")) printf("IPMACC: Synchronizing the region with host\\n");\n'
        code+='clFinish(__ipmacc_command_queue);\n'
        return code
    def openCondition_opencl(self,cond):
        return 'if('+cond+'){\n'
    def closeCondition_opencl(self,cond):
        return '}\n'
    def appendKernelToCode_opencl(self, kerPro, kerDec, kerId, forDims, args, smcinfo):
        #self.code=kerPro+self.code+kerDec
        blockDim=self.blockDim_opencl
        #gridDim='('+'*'.join(forDims)+')/256+1'
        gridDim='(('+forDims+'/'+blockDim+')+1)*'+blockDim
        #callArgs=[]
        #for i in args:
        #    argName=i.split(' ')
        #    argName=argName[len(argName)-1]
        #    callArgs.append(self.varmapper_getDeviceName(self.oacc_kernelsParent[kerId], argName, self.oacc_kernelsAssociatedCopyIds[kerId]))
        # remove undefined declaration from __kernel in three steps: 1) append kernel to code, 2) parse it using cpp, 3) extract the kernel back
        cleanKerDec=''
        for [tp,incstm] in self.code_getAssignments(self.var_parseForYacc(self.code+'\n'+kerDec),['fcn']):
            #if incstm.strip()[0:8]=='__kernel':
            if incstm.strip()[0:100].find('__kernel')!=-1:
                cleanKerDec=incstm
                break
        if cleanKerDec=='':
            print 'Fatal internal error! enable to retrieve back the kernel!'
            exit(-1)
        #print '===================='+kerDec
        #cleanKerDec=statmnts+kerDec
        kerId_str=str(kerId)
        # prepare non-standard types
        type_decls=''
        [intV, intT]=srcml_get_var_details(srcml_code2xml(cleanKerDec),self.prefix_kernel_gen+kerId_str)
        #print 'kernel#'+kerId_str+': '+','.join(intT)
        for [nm, fwdcl, fudcl, oclfudcl] in self.active_types_decl:
            for intTe in intT:
                if intTe.find(nm)!=-1:
                    if DEBUGFWDCL: print 'type is active in this kernel: '+nm
                    type_decls+=oclfudcl+'\n'
                    break
                else:
                    if DEBUGFWDCL: print 'type is inactive in this kernel: '+nm
        # prepare the prototype of function called in the regions
        func_proto=self.getFuncProto_opencl()
        # prepare the declaration of function called in the regions
        func_decl =self.getFuncDecls_opencl()
        # renaming function calls within kernel
        for [fname, prototype, declbody] in self.active_calls_decl:
            cleanKerDec=re.sub('\\b'+fname+'[\\ \\t\\n\\r]*\(','__accelerator_'+fname+'(', cleanKerDec)
        # construct smc calls
        smc_select_calls=''
        if len(smcinfo)>0:
            pfreelist=[]
            for [v, t, st, p, dw, up, div, a, dimlo, dimhi] in smcinfo:
                fcall=self.prefix_kernel_smc_fetch+str(a)+'();'
                if cleanKerDec.find(fcall)==-1:
                    # this smc does not belong to this kernel, ignore
                    continue
                smc_select_calls+='// function identifier \n'+t.replace('*','')+' __smc_select_'+str(a)+'_'+v+'(int index, int down, int up, __global '+t+' g_array, __local '+t+' s_array, int vector_size, int pivot, int before){\n'
                if div=='false':
                    smc_select_calls+='// the pragmas are well-set. do not check the boundaries.\n'
                    smc_select_calls+='return s_array[index-(vector_size*get_group_id(0))+before-pivot];\n'
                else:
                    smc_select_calls+='// The tile is not well covered by the pivot, dw-range, and up-range\n'
                    smc_select_calls+='// dynamic runtime performs the check\n'
                    smc_select_calls+='short a=index>=down;\n'
                    smc_select_calls+='short b=index<up;\n'
                    smc_select_calls+='short d=a&b;\n'
                    smc_select_calls+='if(d){\n'
                    smc_select_calls+='return s_array[index-(vector_size*get_group_id(0))+before-pivot];\n'
                    smc_select_calls+='}\n'
                    smc_select_calls+='return g_array[index];\n'
                smc_select_calls+='}\n'
                pfreelist.append(a)
            for ids in pfreelist:
                fcallst=self.prefix_kernel_smc_fetch+str(ids)+'();'
                fcallen=self.prefix_kernel_smc_fetchend+str(ids)+'();'
                cleanKerDec=cleanKerDec.replace(fcallst,'')
                cleanKerDec=cleanKerDec.replace(fcallen,'')
        # append types, prototypes, and declarations to the kernel string
        cleanKerDec=type_decls+'\n'+func_proto+'\n'+func_decl+'\n'+smc_select_calls+'\n'+cleanKerDec
        # prepare the sting
        cleanKerDec=cleanKerDec.replace('"','\"')
        cleanKerDec=cleanKerDec.replace('\n','\\n')
        kernelInvoc='\n/* kernel call statement*/\n'
        kernelInvoc+='static cl_kernel __ipmacc_clkern'+kerId_str+'=NULL;\n'
        kernelInvoc+='if( __ipmacc_clkern'+kerId_str+'==NULL){\n'
        extensionSupports='#ifdef cl_khr_fp64\\n#pragma OPENCL EXTENSION cl_khr_fp64 : enable\\n#elif defined(cl_amd_fp64)\\n#pragma OPENCL EXTENSION cl_amd_fp64 : enable\\n#else\\n#error \\"Double precision floating point not supported by OpenCL implementation.\\"\\n#endif\\n'
        kernelInvoc+='const char* kernelSource'+kerId_str+' ="'+extensionSupports+cleanKerDec+'";\n'
        kernelInvoc+='cl_program __ipmacc_clpgm'+kerId_str+';\n'
        kernelInvoc+='__ipmacc_clpgm'+kerId_str+'=clCreateProgramWithSource(__ipmacc_clctx, 1, &kernelSource'+kerId_str+', NULL, &__ipmacc_clerr);\n'
        kernelInvoc+=self.checkCallError_opencl('clCreateProgramWithSource','')
        kernelInvoc+='char __ipmacc_clcompileflags'+kerId_str+'[128];\n'
        kernelInvoc+='sprintf(__ipmacc_clcompileflags'+kerId_str+', " ");\n'
        #kernelInvoc+='sprintf(__ipmacc_clcompileflags'+kerId_str+', "-cl-mad-enable");\n'
        exceptionHandler="""
        size_t log_size=1024;
        char *build_log=NULL;
        __ipmacc_clerr=clGetProgramBuildInfo(__ipmacc_clpgm"""+kerId_str+""", __ipmacc_cldevs[0], CL_PROGRAM_BUILD_LOG, 0, NULL, &log_size);
        if(__ipmacc_clerr!=CL_SUCCESS){
            printf("OpenCL Runtime Error in clGetProgramBuildInfo! id: %d\\n",__ipmacc_clerr);
        }
        build_log = (char*)malloc((log_size+1));
        // Second call to get the log
        __ipmacc_clerr=clGetProgramBuildInfo(__ipmacc_clpgm"""+kerId_str+""", __ipmacc_cldevs[0], CL_PROGRAM_BUILD_LOG, log_size, build_log, NULL);
        if(__ipmacc_clerr!=CL_SUCCESS){
            printf("OpenCL Runtime Error in clGetProgramBuildInfo! id: %d\\n",__ipmacc_clerr);
        }
        build_log[log_size] = '\\0';
        printf("--- Build log (%d)---\\n ",log_size);
        fprintf(stderr, "%s\\n", build_log);
        free(build_log);"""
        kernelInvoc+='__ipmacc_clerr=clBuildProgram(__ipmacc_clpgm'+kerId_str+', 0, NULL, __ipmacc_clcompileflags'+kerId_str+', NULL, NULL);\n'
        kernelInvoc+=self.checkCallError_opencl('clBuildProgram',exceptionHandler)
        #kernelInvoc+='cl_kernel __ipmacc_clkern'+kerId_str+' = clCreateKernel(__ipmacc_clpgm'+kerId_str+', "'+self.prefix_kernel_gen+str(kerId_str)+'", &__ipmacc_clerr);\n'
        kernelInvoc+='__ipmacc_clkern'+kerId_str+' = clCreateKernel(__ipmacc_clpgm'+kerId_str+', "'+self.prefix_kernel_gen+str(kerId_str)+'", &__ipmacc_clerr);\n'
        kernelInvoc+='}\n'
        kernelInvoc+=self.checkCallError_opencl('clCreateKernel','')
        for j in range(0,len(args)):
            pointer=(args[j].find('*')!=-1)
            argName=args[j].split(' ')[-1]
            if argName.find('__ipmacc_scalar')!=-1:
                argName='&'+argName
            argName=argName.replace('__ipmacc_scalar','')
            if argName.find('__ipmacc_reductionarray_internal')!=-1:
                argName=self.prefix_kernel_reduction_array+argName
            #argName=args[j].split(' ')[-1].replace('__ipmacc_reductionarray_internal','')
            argName=argName.replace('__ipmacc_reductionarray_internal','')
            argType=' '.join(args[j].split(' ')[0:-1])
            #callArgs.append(self.varmapper_getDeviceName(self.oacc_kernelsParent[kerId], argName, self.oacc_kernelsAssociatedCopyIds[kerId]))
            dname=self.varmapper_getDeviceName(self.oacc_kernelsParent[kerId], argName, self.oacc_kernelsAssociatedCopyIds[kerId])
            if pointer:
                # TODO kernelInvoc+='__ipmacc_clerr=clSetKernelArg(__ipmacc_clkern'+kerId_str+', '+str(j)+', sizeof(cl_mem), (void *)&'+dname+');\n'
                if argName.find('__ipmacc_deviceptr')==-1:
                    kernelInvoc+='{\ncl_mem ptr=(cl_mem)acc_deviceptr('+argName+');\n__ipmacc_clerr=clSetKernelArg(__ipmacc_clkern'+kerId_str+', '+str(j)+', sizeof(cl_mem), (void *)&ptr);\n}\n'
                else:
                    kernelInvoc+='{\ncl_mem ptr=(cl_mem)'+argName+';\n__ipmacc_clerr=clSetKernelArg(__ipmacc_clkern'+kerId_str+', '+str(j)+', sizeof(cl_mem), (void *)&ptr);\n}\n'
            else:
                #kernelInvoc+='__ipmacc_clerr=clSetKernelArg(__ipmacc_clkern'+kerId_str+', '+str(j)+', sizeof('+argType.replace('*','')+'), (void *)&'+dname+');\n'
                kernelInvoc+='{\n'+argType.replace('*','')+' immediate='+argName+';\n__ipmacc_clerr=clSetKernelArg(__ipmacc_clkern'+kerId_str+', '+str(j)+', sizeof('+argType.replace('*','')+'), (void *)&immediate);\n}\n'
            kernelInvoc+=self.checkCallError_opencl('clSetKernelArg','')
        kernelInvoc+=('if (getenv("IPMACC_VERBOSE")) printf("IPMACC: Launching kernel '+kerId_str+' > gridDim: %d\\tblockDim: %d\\n",'+gridDim+','+blockDim+');\n')
        kernelInvoc+='size_t global_item_size'+kerId_str+' = '+gridDim+';\n'
        kernelInvoc+='size_t local_item_size'+kerId_str+' = '+blockDim+';\n'
        kernelInvoc+='__ipmacc_clerr=clEnqueueNDRangeKernel(__ipmacc_command_queue, __ipmacc_clkern'+kerId_str+', 1, NULL,\n &global_item_size'+kerId_str+', &local_item_size'+kerId_str+', 0, NULL, NULL);\n'
        kernelInvoc+=self.checkCallError_opencl('clEnqueueNDRangeKernel','')
        #kernelInvoc+=self.prefix_kernel_gen+str(kerId)+'<<<'+gridDim+','+blockDim+'>>>('+(','.join(callArgs))+');'
        kernelInvoc+='\n/* kernel call statement*/\n'
        #self.code=self.code.replace(self.prefix_kernel+kerId_str+'();',kernelInvoc)
        self.code_kernels.append(kernelInvoc)
    def reduceVariable_opencl(self, var, type, op, ctasize):
        arrname=self.prefix_kernel_reduction_shmem+type
        iterator=self.prefix_kernel_reduction_iterator
        code ='\n/* reduction on '+var+' */\n'
        code+='barrier(CLK_LOCAL_MEM_FENCE /*| CLK_GLOBAL_MEM_FENCE*/);\n'
        code+=arrname+'[get_local_id(0)]='+var+';\n';
        code+='barrier(CLK_LOCAL_MEM_FENCE /*| CLK_GLOBAL_MEM_FENCE*/);\n'

        # ALTERIMPLEMENTATION
        # ALTER 1 
        #code+='for('+iterator+'='+ctasize+'; '+iterator+'>1; '+iterator+'='+iterator+'/2){\n'
        #code+='if(get_local_id(0)<'+iterator+' && get_local_id(0)>='+iterator+'/2){\n'
        #des=arrname+'[get_local_id(0)-('+iterator+'/2)]'
        #src=arrname+'[get_local_id(0)]'
        #if op=='min':
        #    code+=des+'=('+(des+'>'+src)+'?'+(src)+':'+(des)+');\n'
        #elif op=='max':
        #    code+=des+'=('+(des+'>'+src)+'?'+(des)+':'+(src)+');\n'
        #else:
        #    code+=des+'='+des+op+src+';\n'
        #code+='}\n'
        #code+='barrier(CLK_LOCAL_MEM_FENCE /*| CLK_GLOBAL_MEM_FENCE*/);\n'
        #code+='}\n'
        # ALTER 2
        code+='for('+iterator+'='+ctasize+'/2;'+iterator+'>0; '+iterator+'>>=1) {\n'
        code+='if(get_local_id(0)<'+iterator+'){\n'
        src=arrname+'[get_local_id(0)+'+iterator+']'
        des=arrname+'[get_local_id(0)]'
        if op=='min':
            code+=des+'=('+(des+'>'+src)+'?'+(src)+':'+(des)+');\n'
        elif op=='max':
            code+=des+'=('+(des+'>'+src)+'?'+(des)+':'+(src)+');\n'
        else:
            code+=des+'='+des+op+src+';\n'
        code+='}\n'
        code+='barrier(CLK_LOCAL_MEM_FENCE /*| CLK_GLOBAL_MEM_FENCE*/);\n'
        code+='}\n'
        # END OF ALTER

        code+='}// the end of '+var+' scope\n'
        # this reduction works for most devices, but can be implemented efficienctly considering device specific atomic operations
        #code+='/*atomicAdd('+var+','+var+'[0]+'+arrname+'[0]);\n\n*/'
        code+='if(get_local_id(0)==0){\n'
        if REDUCTION_TWOLEVELTREE:
            code+=var+'__ipmacc_reductionarray_internal[get_group_id(0)]='+arrname+'[0];\n'
        else:
            self.code_include+='__global unsigned long long int '+self.prefix_kernel_reduction_lock+var+'=0u;\n'
            code+='while (atomicCAS(&'+self.prefix_kernel_reduction_lock+var+', 0u, 1u)==1u){\n'
            code+='};\n'
            code+='//start global critical secion\n'
            des=var+'[0]'
            src=arrname+'[0]'
            if op=='min':
                code+=des+'=('+(des+'>'+src)+'?'+(src)+':'+(des)+');\n'
            elif op=='max':
                code+=des+'=('+(des+'>'+src)+'?'+(des)+':'+(src)+');\n'
            else:
                code+=des+'='+des+op+src+';\n'
            code+=self.prefix_kernel_reduction_lock+var+'=0u;\n'
            code+='//^D end global critical secion\n'
        code+='}\n'
        return code
    def constructKernel_opencl(self, args, decl, kernelB, kernelId, privinfo, reduinfo, ctasize, forDims, template, smcinfo):
        code =template+' __kernel void '+self.prefix_kernel_gen+str(kernelId)
        suff_args=[]
        for idx in range(0,len(args)):
            sc=args[idx].replace('__ipmacc_deviceptr','')
            if sc.count('*')!=0:
                suff_args.append('__global '+sc)
            else:
                suff_args.append(sc)
        code+='('+','.join(suff_args)+')'
        proto=code+';\n'
        code+='{\n'
        code+='int '+self.prefix_kernel_uid+'=get_global_id(0);\n'
        # fetch __ipmacc_scalar into register
        for sc in args:
            if sc.find('__ipmacc_scalar')!=-1:
                vname=sc.split(' ')[-1]
                type=sc.replace(vname,'').replace('*','')
                code+=type+' '+vname.replace('__ipmacc_scalar','')+' = '+vname+'[0];\n'
        #code+='if('+self.prefix_kernel_uid+'>='+forDims+'){\nreturn;\n}\n'
        if len(reduinfo+privinfo)>0:
            # 1) serve privates
            pfreelist=[]
            for [v, i, o, a, t] in privinfo:
                fcall=self.prefix_kernel_privred_region+str(a)+'();'
                scp=('{ //start of reduction region for '+v+' \n') if o!='U' else ''
                kernelB=kernelB.replace(fcall,scp+t+' '+v+'='+i+';\n'+fcall)
                pfreelist.append(a)
            for ids in pfreelist:
                fcall=self.prefix_kernel_privred_region+str(ids)+'();'
                kernelB=kernelB.replace(fcall,'');
            # 2) serve reductions
            decl+='int '+self.prefix_kernel_reduction_iterator+'=0;\n'
            types=[] # types to reserve space for fast shared-memory reductions
            rfreelist=[] #remove reduction calls
            reduinfo.reverse()
            for [v, i, o, a, t] in reduinfo:
                fcall=self.prefix_kernel_reduction_region+str(a)+'();'
                # 2) 1) append proper reduction code for this variable
                kernelB=kernelB.replace(fcall,self.codegen_reduceVariable(v,t,o,ctasize)+fcall)
                types.append(t)
                rfreelist.append(a)
                decl+=t+' '+v+';'
            reduinfo.reverse()
            # 2) 2) allocate shared memory reduction array
            types=list(set(types))
            for t in types:
                code=code+'__local '+t+' '+self.prefix_kernel_reduction_shmem+t+'['+ctasize+'];\n'
            rfreelist=list(set(rfreelist))
            # 2) 3) free remaining fcalls
            for ids in rfreelist:
                fcall=self.prefix_kernel_reduction_region+str(ids)+'();'
                kernelB=kernelB.replace(fcall,'')
        smc_select_calls=''
        if len(smcinfo)>0:
            #pfreelist=[]
            for [v, t, st, p, dw, up, div, a, dimlo, dimhi] in smcinfo:
                fcall=self.prefix_kernel_smc_fetch+str(a)+'();'
                if kernelB.find(fcall)==-1:
                    # this smc does not belong to this kernel, ignore 
                    continue
                length=self.blockDim_opencl+'+'+dw+'+'+up
                decl+='\n/* declare the local memory of '+v+' */\n'
                decl+='__local '+t.replace('*','')+' '+self.prefix_kernel_smc_varpref+v+'['+length+'];\n'
                decl+='__local unsigned char '+self.prefix_kernel_smc_tagpref+v+'['+length+'];\n'
                decl+='{\n'
                decl+='int iterator_of_smc=0;\n'
                decl+='for(iterator_of_smc=get_local_id(0); iterator_of_smc<('+length+'); iterator_of_smc+=get_local_size(0)){\n'
                decl+=self.prefix_kernel_smc_varpref+v+'[iterator_of_smc]=0;\n'
                decl+=self.prefix_kernel_smc_tagpref+v+'[iterator_of_smc]=0;\n'
                decl+='}\nbarrier(CLK_LOCAL_MEM_FENCE);\n'
                decl+='}\n'
                # fetch data to local memory
                datafetch ='{ // fetch begins\nint kk;\n'
                datafetch+='barrier(CLK_LOCAL_MEM_FENCE);\n'
                datafetch+='for(int kk=get_local_id(0); kk<('+length+'); kk+=get_local_size(0))\n'
                datafetch+='{\n'
                datafetch+='int idx=get_group_id(0)*'+self.blockDim_opencl+'+kk-'+dw+'+'+p+';\n'
                datafetch+='if(idx<('+dimhi+') && idx>=('+dimlo+'))\n'
                datafetch+='{\n'
                datafetch+=self.prefix_kernel_smc_varpref+v+'[kk]='+v+'[idx];\n'
                datafetch+=self.prefix_kernel_smc_tagpref+v+'[kk]=1;\n'
                datafetch+='}\n'
                datafetch+='}\n'
                datafetch+='barrier(CLK_LOCAL_MEM_FENCE);\n'
                datafetch+='} // end of fetch\n'
                datafetch+='#define '+v+'(index) __smc_select_'+str(a)+'_'+v+'(index, (get_group_id(0)*'+self.blockDim_opencl+')-('+dw+'), ((get_group_id(0)+1)*'+self.blockDim_opencl+')+('+up+'), '+v+', '+self.prefix_kernel_smc_varpref+v+', '+self.blockDim_opencl+', '+p+', '+dw+')\n'
                kernelB=kernelB.replace(fcall,datafetch+'\n'+fcall)
                # construct the smc_select_ per array
                # following operations are performed in appendKernelToCode_opencl
                #smc_select_calls+='// function identifier \n'+t.replace('*','')+' __smc_select_'+str(a)+'_'+v+'(int index, int down, int up, '+t+' g_array, '+t+' s_array, int vector_size, int pivot, int before){\n'
                #if div=='false':
                #    smc_select_calls+='// the pragmas are well-set. do not check the boundaries.\n'
                #    smc_select_calls+='return s_array[index-(vector_size*get_group_id(0))+before-pivot];\n'
                #else:
                #    smc_select_calls+='// The tile is not well covered by the pivot, dw-range, and up-range\n'
                #    smc_select_calls+='// dynamic runtime performs the check\n'
                #    smc_select_calls+='short a=index>=down;\n'
                #    smc_select_calls+='short b=index<up;\n'
                #    smc_select_calls+='short d=a&b;\n'
                #    smc_select_calls+='if(d){\n'
                #    smc_select_calls+='return s_array[index-(vector_size*get_group_id(0))+before-pivot];\n'
                #    smc_select_calls+='}\n'
                #    smc_select_calls+='return g_array[index];\n'
                #smc_select_calls+='}\n'
                # replace array-ref [] with function call ()
                fcallst=self.prefix_kernel_smc_fetch+str(a)+'();'
                fcallen=self.prefix_kernel_smc_fetchend+str(a)+'();'
                changeRangeIdx_start=kernelB.find(fcallst)
                changeRangeIdx_end=kernelB.find(fcallen)
                #print kernelB[changeRangeIdx_start:changeRangeIdx_end]
                if (changeRangeIdx_start==-1 ) or (changeRangeIdx_end==-1) or (changeRangeIdx_start>changeRangeIdx_end):
                    print 'fatal error! could not determine the smc range for '+v
                    exit(-1)
                # for each arrayReference of 'v', replace [] with ()
                for arrayRef in re.finditer('\\b'+v+'[\\ \\t\\n\\r]*\[',kernelB[changeRangeIdx_start:changeRangeIdx_end]):
                    arrayRef_it=changeRangeIdx_start+arrayRef.start(0)
                    arrayRef_pcnt=0
                    done=False
                    while not done:
                        if kernelB[arrayRef_it]=='[':
                            if arrayRef_pcnt==0:
                                #kernelB[arrayRef_it]='('
                                kernelB=kernelB[:arrayRef_it]+'('+kernelB[arrayRef_it+1:]
                            arrayRef_pcnt+=1
                        elif kernelB[arrayRef_it]==']':
                            arrayRef_pcnt-=1
                            if arrayRef_pcnt==0:
                                #kernelB[arrayRef_it]=')'
                                kernelB=kernelB[:arrayRef_it]+')'+kernelB[arrayRef_it+1:]
                                done=True
                        arrayRef_it+=1
                     
                # undef function call ()
                kernelB=kernelB.replace(fcallen,'#undef '+v+'\n'+fcallen)
                #pfreelist.append(a)
            #for ids in pfreelist:
            #    fcallst=self.prefix_kernel_smc_fetch+str(ids)+'();'
            #    fcallen=self.prefix_kernel_smc_fetchend+str(ids)+'();'
            #    kernelB=kernelB.replace(fcallst,'')
            #    kernelB=kernelB.replace(fcallen,'')
        #print 'smc_select_calls:> '+smc_select_calls
        #code=smc_select_calls+'/* HOHA */\n'+code
        code+=decl
        code+=kernelB
        code+='}\n'
        return [proto, code]
    def memAlloc_opencl(self, var, size):
        codeM=var+' = clCreateBuffer(__ipmacc_clctx, CL_MEM_READ_WRITE, '+size+', NULL, &__ipmacc_clerr);\n'
        codeM+=self.checkCallError_opencl('clCreateBuffer','')
        return codeM
    def memCpy_opencl(self, des, src, size, type):
        if type=='in':
            codeC='clEnqueueWriteBuffer(__ipmacc_command_queue, '+des+', CL_TRUE, 0, '+size+','+src+', 0, NULL, NULL);\n'
            codeC+=self.checkCallError_opencl('clEnqueueWriteBuffer','')
        else:
            codeC='clEnqueueReadBuffer(__ipmacc_command_queue, '+src+', CL_TRUE, 0, '+size+','+des+', 0, NULL, NULL);\n'
            codeC+=self.checkCallError_opencl('clEnqueueReadBuffer','')
        return codeC
    def devPtrDeclare_opencl(self, type, name, sccopy):
        #return 'cl_mem'+('* ' if sccopy else ' ')+name+';\n'
        return 'cl_mem '+name+';\n'
    def checkCallError_opencl(self,fcn,expt):
        code ='if(__ipmacc_clerr!=CL_SUCCESS){\n'
        code+='printf("OpenCL Runtime Error in '+fcn+'! id: %d\\n",__ipmacc_clerr);\n'
        code+=expt
        code+='exit(-1);\n'
        code+='}\n'
        return code
    def getFuncDecls_opencl(self):
        code=''
        for [fname, prototype, declbody] in self.active_calls_decl:
            code +=declbody+'\n'
        for [fname, prototype, declbody] in self.active_calls_decl:
            code=re.sub('\\b'+fname+'[\\ \\t\\n\\r]*\(','__accelerator_'+fname+'(', code)
        return code
    def getFuncProto_opencl(self):
        code=''
        for [fname, prototype, declbody] in self.active_calls_decl:
            code +=prototype+'\n'
        for [fname, prototype, declbody] in self.active_calls_decl:
            code=re.sub('\\b'+fname+'[\\ \\t\\n\\r]*\(','__accelerator_'+fname+'(', code)
        return code

    # Marking for final replacement
    def mark_implicitcopy(self,inout,kid):
        return self.prefix_dataimpli+inout+str(kid)+'();'

    #
    # Top Level Recursive Code Analyzer
    def code_descendentRetrieve(self, root, depth, associated_copy_ids):
        # parse the code's XML tree (root) and retrieve the intermediate code (self.code)
        scope_associated_copy_ids=[]
        scope_associated_copy_ids+=associated_copy_ids
        if root.tag == 'pragma' and root.attrib.get('directive')=='kernels':
            # case 1: start of the kernel region
            # parse the clause for data (including copy, copyin, copyout, create, and similar present alternatives
            expressionIn=''
            expressionAlloc=''
            expressionOut=''
            expressionAll=''
            copyoutId=-1
            [expressionIn, expressionAlloc, expressionOut, expressionAll] = self.oacc_clauseparser_data(str(root.attrib.get('clause')),str(self.oacc_copyId))
            if DEBUGVAR:
                print 'Kernels data clause: <'+expressionIn+'\n'+expressionAlloc+'\n'+expressionOut+'>' # expressionIn format: varname="a" in="true" present="true" dim0="0:SIZE"
                print 'all data clauses: <'+expressionAll+'>'
            # * generate proper code before the kernels region:
            #   - if
            regionCondition=self.oacc_clauseparser_if(str(root.attrib.get('clause')))
            if regionCondition!='':
                self.code=self.code+self.codegen_openCondition(regionCondition)
            #   - copy, copyin (allocation and transfer)
# HERE
            #self.util_copyIdAppend(expressionIn, expressionAlloc, expressionOut, depth)
            copyoutId=self.util_copyIdAppend(expressionIn, expressionAlloc, expressionOut, depth, expressionAll)
            #print 'kernels: appending '+str(copyoutId)
            scope_associated_copy_ids+=[copyoutId]
#            if expressionIn!='':
#                self.code=self.code+('\t'*depth)+self.prefix_dataalloc+str(self.oacc_copyId)+'();'
#                self.code=self.code+('\t'*depth)+self.prefix_datacp+str(self.oacc_copyId)+'();'
#                self.oacc_copys.append([self.oacc_kernelId,expressionIn])
#                self.oacc_copyId=self.oacc_copyId+1
#            #   - create (allocation)
#            if expressionAlloc!='':
#                self.code=self.code+('\t'*depth)+self.prefix_dataalloc+str(self.oacc_copyId)+'();'
#                self.code=self.code+('\t'*depth)+self.prefix_datacp+str(self.oacc_copyId)+'();'
#                self.oacc_copys.append([self.oacc_kernelId,expressionAlloc])
#                self.oacc_copyId=self.oacc_copyId+1
#            #   - copy, copyout (allocation)
#            if expressionOut!='':
#                self.code=self.code+('\t'*depth)+self.prefix_dataalloc+str(self.oacc_copyId)+'();'
#                copyoutId=self.oacc_copyId
#                self.oacc_copys.append([self.oacc_kernelId,expressionOut])
#                self.oacc_copyId=self.oacc_copyId+1
# TO HERE
            #   - track automatic vars (deviceptr)
            expressionDeviceptrs=self.oacc_clauseparser_deviceptr(str(root.attrib.get('clause')))
            if expressionDeviceptrs!='' or self.oacc_scopeAutomaPtr!='':
                # append in either case
                if DEBUGVAR:
                    print 'appending automatic vars: '+(expressionDeviceptrs+' '+self.oacc_scopeAutomaPtr).strip().replace(' ',',')
                self.oacc_kernelsAutomaPtrs.append((expressionDeviceptrs+' '+self.oacc_scopeAutomaPtr).strip().replace(' ',','))
            else:
                self.oacc_kernelsAutomaPtrs.append('')
            #   - track manual vars (copy in, copy out, and create)
            expressionManualVars=self.varname_extractor(expressionAll)
            #expressionManualVars=self.varname_extractor(expressionIn+'\n'+expressionOut+'\n'+expressionAlloc)
            if DEBUGVAR:
                print 'Extracted manual variable names > '+expressionManualVars
            if expressionManualVars!='' or self.oacc_scopeManualPtr!='':
                # append in either case
                if DEBUGCP>1:
                    print 'kernelManualPtrs: '+(expressionManualVars+' '+self.oacc_scopeManualPtr).strip().replace(' ',',')
                self.oacc_kernelsManualPtrs.append((expressionManualVars+' '+self.oacc_scopeManualPtr).strip().replace(' ',','))
            else:
                self.oacc_kernelsManualPtrs.append('')
            #   - speculative implicit memory allocation/transfers
            self.code=self.code+self.mark_implicitcopy('in',self.oacc_kernelId)
            # * generate dummy kernel launch function call
            self.code=self.code+self.prefix_kernel+str(self.oacc_kernelId)+'();'
            self.carry_loopAttr2For(root,False,[],[],'','',[])
            self.oacc_kernels.append(root)
            # * generate proper code after the kernels region:
            #   - copy, copyout (transfer)
            if copyoutId!=-1: #expressionAll!='':
                self.code=self.code+('\t'*depth)+self.prefix_datacpout+str(copyoutId)+'();'
            #   - speculative implicit memory allocation/transfers
            self.code=self.code+self.mark_implicitcopy('out',self.oacc_kernelId)
            #   - async
            if not self.oacc_clauseparser_flags(str(root.attrib.get('clause')),'async'):
                self.code=self.code+self.codegen_syncDevice()
            #   - if
            if regionCondition!='':
                self.code=self.code+self.codegen_closeCondition(regionCondition)
            # * finilize state
            self.oacc_kernelId=self.oacc_kernelId+1
            self.oacc_kernelsAssociatedCopyIds.append(scope_associated_copy_ids)
        elif root.getchildren()==[]:
            # case 2: no descendent is found
            if root.tag == 'for':
                # for is special case, handle it specially
                self.code=self.code+str('\t'*depth)+'for('+str(root.attrib.get('initial'))+';'+str(root.attrib.get('boundary'))+';'+str(root.attrib.get('increment'))+')'
            self.code=self.code+str(root.text)
        else:
            # case 3: go through descendents recursively
            expressionIn=''
            expressionAlloc=''
            expressionOut=''
            expressionAll=''
            copyoutId=-1
            temp_scopeAutoma=''
            temp_scopeManual=''
            if root.tag == 'for':
                self.code=self.code+str('\t'*depth)+'for('+str(root.attrib.get('initial'))+';'+str(root.attrib.get('boundary'))+';'+str(root.attrib.get('increment'))+')'
            elif (root.tag=='pragma' and root.attrib.get('directive')=='data'):
                # parse data clauses and
                [expressionIn, expressionAlloc, expressionOut, expressionAll] = self.oacc_clauseparser_data(str(root.attrib.get('clause')),str(self.oacc_copyId))
                if DEBUGCP>0:
                    print expressionIn+'\n'+expressionAlloc+'\n'+expressionOut # expressionIn format: varname="a" in="true" present="true" dim0="0:SIZE"
                    print 'all data clauses: '+expressionAll
                # dump pragma copyin allocation/transfer before region
# HERE
                copyoutId=self.util_copyIdAppend(expressionIn, expressionAlloc, expressionOut, depth, expressionAll)
                #print 'data: appending '+str(copyoutId)
                scope_associated_copy_ids+=[copyoutId]
                #if expressionIn!='':
                #    self.code=self.code+('\t'*depth)+self.prefix_dataalloc+str(self.oacc_copyId)+'();'
                #    self.code=self.code+('\t'*depth)+self.prefix_datacp+str(self.oacc_copyId)+'();'
                #    self.oacc_copys.append([self.oacc_kernelId,expressionIn])
                #    self.oacc_copyId=self.oacc_copyId+1
                ## dump pragma create allocation before region
                #if expressionAlloc!='':
                #    self.code=self.code+('\t'*depth)+self.prefix_dataalloc+str(self.oacc_copyId)+'();'
                #    self.code=self.code+('\t'*depth)+self.prefix_datacp+str(self.oacc_copyId)+'();'
                #    self.oacc_copys.append([self.oacc_kernelId,expressionAlloc])
                #    self.oacc_copyId=self.oacc_copyId+1
                ## dump pragma copyout allocation before region
                #if expressionOut!='':
                #    self.code=self.code+('\t'*depth)+self.prefix_dataalloc+str(self.oacc_copyId)+'();'
                #    copyoutId=self.oacc_copyId
                #    self.oacc_copys.append([self.oacc_kernelId,expressionOut])
                #    self.oacc_copyId=self.oacc_copyId+1
# TO HERE
                #   - automatic variables [deviceptr] (update deviceptr variable of this scope, if anything is defined)
                temp_scopeAutoma=self.oacc_clauseparser_deviceptr(str(root.attrib.get('clause')))
                if temp_scopeAutoma!='':
                    self.oacc_scopeAutomaPtr=self.oacc_scopeAutomaPtr+temp_scopeAutoma+' '
                #   - manual variables (explicit copies)
                #temp_scopeManual=self.varname_extractor(expressionIn+'\n'+expressionOut+'\n'+expressionAlloc)
                temp_scopeManual=self.varname_extractor(expressionAll)
                # print temp_scopeManual
                if temp_scopeManual!='':
                    self.oacc_scopeManualPtr=self.oacc_scopeManualPtr+temp_scopeManual+' '
            for child in root:
                self.code_descendentRetrieve(child,depth+1,scope_associated_copy_ids)
            # dump pragma copyout transfer after the region
            if (root.tag=='pragma' and root.attrib.get('directive')=='data') and copyoutId!=-1:
                # dump pragma transfer after region
                self.code=self.code+('\t'*depth)+self.prefix_datacpout+str(copyoutId)+'();'
                #   - automatic variables [deviceptr]
                if temp_scopeAutoma!='':
                    # subtract this scope automatic variables
                    self.oacc_scopeAutomaPtr=self.replace_last(self.oacc_scopeAutomaPtr, temp_scopeAutoma+' ', '')
                #   - manual variables
                if temp_scopeManual!='':
                    # subtract this scope manual variables
                    self.oacc_scopeManualPtr=self.replace_last(self.oacc_scopeManualPtr, temp_scopeManual+' ', '')

    def code_descendentDump(self,filename):
        # dump the code at current stage to filename
        old_stdout = sys.stdout
        f = open(filename,'w')
        sys.stdout = f
        print self.code_include+self.code
        f.close()
        sys.stdout = old_stdout
        if ENABLE_INDENT==True:
            Popen(["indent", filename])
    def code_getAssignments(self,code,specialRet=[]):
        # parse the code and break it into top-level assignments:
        # function declaration, type declaration, prototying,
        statements=[]
        #[sttyp,ststr,start,unknown,inc,defi,typdec]=['udf','',True,False,False,False,False]
        [sttyp,ststr,start,incdef]=['udf','',True,False]
        # sttyp: udf undefined, fcn function, ukw unknown-directive, inc include-directive, def define-directive, typ typedef-or-struct-declaration, 
        openpar=0
        for idx in range(0,len(code)):
            ch=code[idx]
            ststr+=ch
            stmend=False
            # start string control
            if start==True and (ch==' ' or ch=='\n' or ch=='\t'):
                continue
            elif start==True:
                start=False
                # non-whitespace start of statement
                if ch=='#':
                    #print 'given char> '+code[idx+1:idx+20].strip()[0:7]
                    incdef=True
                    if   code[idx+1:idx+20].strip()[0:6]=='define':
                        sttyp='def'
                    elif code[idx+1:idx+20].strip()[0:7]=='include':
                        sttyp='inc'
                    else:
                        sttyp='ukw'
                else:
                    if   code[idx:idx+20].strip()[0:7]=='typedef':
                        sttyp='typ'
                    elif code[idx:idx+20].strip()[0:6]=='struct':
                        sttyp='str'
            # process ch
            if ch=='{':
                openpar+=1
            elif ch=='}':
                openpar-=1
            if (openpar==0 and ch=='}') or (openpar==0 and ch==';') or (incdef and ch=='\n'):
                stmend=True
            # check for type
            if ch=='(' and openpar==0 and sttyp=='udf':
                sttyp='fcn'
            # statement termination check
            if stmend:
                skip=True
                if len(specialRet)==0:
                    skip=False
                else:
                    for itm in specialRet:
                        if sttyp==itm:
                            skip=False
                if not skip:
                    statements.append([sttyp,ststr.strip()])
                [sttyp,ststr,start,incdef]=['udf','',True,False]
        return statements
    #
    # VARIABLE TYPE DETECTOR FUNCTIONS: var_kernel_parentsFind, var_copy_parentsFind, var_findFuncParents, var_parseForYacc,
    def astCalcRoot(self):
        if USEPYCPARSER:
            text = self.var_parseForYacc(self.code)
            if DEBUGCPARSER>0:
                print text
            # create a pycparser
            parser = c_parser.CParser()
            ast = parser.parse(text, filename='<none>')

            # generate the XML tree
            if DEBUGCPARSER>0:
                ast.show()
            codeAstXml = open('code_ast.xml','w')
            ast.showXml(codeAstXml)
            codeAstXml.close()
            tree = ET.parse('code_ast.xml')
            os.remove('code_ast.xml')
            self.astRoot = tree.getroot()
        else:
            #srcML
            self.astRootML = srcml_code2xml(self.code)
            if DEBUGSRCMLC: print 'Error 1019! Unimplemented AST generator!'
            exit(-1)

    def pycparserGetWritesTo(self,code):
        text = self.var_parseForYacc(code)
        print text
        parser = c_parser.CParser()
        ast = parser.parse(text, filename='<none>')


    def var_kernel_parentsFind(self):
        self.var_findFuncParents("kernel")

    def var_copy_parentsFind(self):
        self.var_findFuncParents("data")
        if len(self.oacc_copysVarNams)!=self.oacc_copyId or len(self.oacc_copysVarTyps)!=self.oacc_copyId:
            print 'internal error! could not determine the parent function of data copy statement!'
            exit(-1)
    
    def var_findFuncParents(self,funcName):
        # find the parent of function
        # parent of function A is a function calling A
        # here, the parent is unique since the funcName is unique autogenerated name
        if USEPYCPARSER:
            root = self.astRoot
        else:
            # srcML
            root = self.astRootML
            if DEBUGSRCMLC: print 'Error 1040! Unimplemented AST parser!'
            #exit(-1)
        
        fname=''
        count  = self.oacc_kernelId if funcName=="kernel" else self.oacc_copyId
        prefix = self.prefix_kernel if funcName=="kernel" else self.prefix_datacpin
        for id in range(0,count):
            # go through all functions in the code (C/C++ code)
            # find the function which the function is called there
            # then find the type of all variables
            kn=prefix+str(id)
            funcVars=[]
            funcTyps=[]
            if USEPYCPARSER:
                for func in root.findall(".//FuncDef"):
                    funcFound=0
                    # print('we have found '+str(len(func.findall(".//FuncCall/ID")))+' function calls in '+str(func.find('Decl').get('uid')))
                    for fcall in func.findall(".//FuncCall/ID"):
                        if str(fcall.get('uid')).strip()==kn.strip():
                            funcFound=1
                            fname=func.find('Decl').get('uid')
                            if DEBUGFC:
                                fname=self.wrapFuncName(fname)
                                print 'function name> '+fname
                    if funcFound==1:
                        # print('<'+kn+'> is found in <'+func.find('Decl').get('uid')+'>')
                        # go through all declerations and find the varibales
                        # first, function prototype
                        funcBody=func.find('Compound')              # variable defined in the body
                        if func.find('.//ParamList'):
                            funcBody.append(func.find('.//ParamList'))  # variables defined in the params
                        for var in funcBody.findall(".//Decl"):
                            # single variable Decl
                            declP=''
                            for chl in var:
                                declP=tostring(chl)
                                if DEBUGCP>1:
                                    print var.get('uid').split(',')[0]+'->'
                                    print '\t>'+declP
                                break
                            funcVars.append(var.get('uid').split(',')[0])
                            #funcTyps.append(var.find('.//IdentifierType').get('uid')+((len(var.findall(".//PtrDecl"))+len(var.findall(".//ArrayDecl")))*'*'))
                            funcTyps.append(var.find('.//IdentifierType').get('uid')+((declP.count("<PtrDecl")+declP.count("<ArrayDecl>"))*'*'))
                            if DEBUGCP>1:
                                #print('< '+var.get('uid')+' > is defined as <'+var.find('.//IdentifierType').get('uid')+((len(var.findall(".//PtrDecl")))*'*')+'>')
                                print('< '+var.get('uid')+' > is defined as <'+var.find('.//IdentifierType').get('uid')+((declP.count("<PtrDecl"))*'*')+'>')
                        
                        break
            else:
                # srcML
                [template,fname]=srcml_get_parent_fcn(root,kn.strip())
                [fnV, fnT]=srcml_get_var_details(root, fname)
                if DEBUGCPARSER>0:
                    print 'declared  vars > '+','.join(fnV)
                    print 'declared types > '+','.join(fnT)
                self.forward_declare_append_new_types(fnT)
                funcVars=fnV
                funcTyps=fnT
                if DEBUGSRCMLC: print 'Error 1093! unimplemented AST parser!'
                #exit(-1)
            # make sure functionParent is found
            if fname=='':
                print 'Fatal Internal Error!'
                print 'could not find the generated function'
                print '\t'+kn.strip()+' is not called in following XML tree:'
                print tostring(root)
                exit(-1)
            fname=self.wrapFuncName(fname)
            if DEBUGFC:
                print kn.strip()+' is called in '+fname
            # At this point we have fname, funcVars, funcTypes here
            if funcName=="kernel":
                self.oacc_kernelsVarNams.append(funcVars)
                self.oacc_kernelsVarTyps.append(funcTyps)
                self.oacc_kernelsParent.append(fname)
                self.oacc_kernelsTemplates.append(template)
            else:
                self.oacc_copysVarNams.append(funcVars)
                self.oacc_copysVarTyps.append(funcTyps)
                self.oacc_copysParent.append(fname) 

    # YACC-friendly code generator
    def var_parseForYacc(self, InCode):
        # here  the InCode has no comment block or comment line
        # 1) instead of removing include, we put a workout:
        code="#define __attribute__(x)\n"+"#define __asm__(x)\n"+"#define __builtin_va_list int\n"+"#define __const\n"+"#define __restrict\n"+"#define __extension__\n"+"#define __inline__\n"+InCode
        #code = InCode
        #re.sub(r'(#include).*.(\n)', '', code)
        code=self.preprocess_by_gnu_cpp(code)
        return code.strip()

    def argument_parser(self):
        args=[]
        if DEBUGCPP: print 'printing args <'+self.nvcc_args+'>'
        skip=False
        capture=False
        for arg in self.nvcc_args.split():
            if skip:
                skip=False
                continue
            if capture:
                capture=False
                args.append(arg)
            ch=arg[0:2]
            if   ch=='-D' or ch=='-I':
                args.append(arg)
                if arg=='-I': capture=True #swallow the next argument blindly
            elif ch=='-o':
                skip=True
        if DEBUGCPP: print '\targs> '+', '.join(args)
        return args


    def preprocess_by_gnu_cpp(self, codein):
        f = tempfile.NamedTemporaryFile(delete=False)
        f.write(codein)
        f.close()
        # 2) replace #define and unroll #include using GNU cpp 
        if DEBUGCPP:
            print('opening input file <'+f.name+'>')
            print('cat '+f.name+' | '+"cpp -E -I"+os.path.dirname(os.path.realpath(__file__))+"/../include/ -I"+os.path.dirname(self.foname))
            #exit(-1)
        cpp_call =["cpp", "-x", "c++", "-E", "-I"+os.path.dirname(os.path.realpath(__file__))+"/../include/", "-I"+os.path.dirname(self.foname)+"/./"]
        cpp_call+=self.argument_parser()
        if DEBUGCPP: print 'cpp call: '+', '.join(cpp_call)

        p1 = Popen(["cat", f.name], stdout=PIPE)
        #p2 = Popen(["cpp", "-x", "c++", "-E", "-I"+os.path.dirname(os.path.realpath(__file__))+"/../include/", "-I"+os.path.dirname(self.foname)+"/./"], stdin=p1.stdout, stdout=PIPE)
        p2 = Popen(cpp_call, stdin=p1.stdout, stdout=PIPE)
        code = p2.communicate()[0]
        os.remove(f.name)
        # 3) remove cpp # in the begining of file
        code=re.sub(r'(#\ ).*.(\n)', '', code)
        code=code.replace("extern \"C\"",'');
        return code

    def assignmentRecursive(self,astNode):
        print('Not implemented!')

    def declareRecursive(self,astNode):
        # find the size of variable declered by astNode
        code=''
        if astNode.tag=='PtrDecl':
            # one child
            code='(dynamic)*'+self.declareRecursive(astNode[0])
        elif astNode.tag=='ArrayDecl' and len(astNode)==2:
            # array of known size
            code='('+self.declareRecursive(astNode[1])+')*'+self.declareRecursive(astNode[0])
        elif astNode.tag=='ArrayDecl' and len(astNode)==1:
            # array of unkown size
            # potentially function argument or dynamic allocation
            # so assume it as dynamic
            code='(dynamic)*'+self.declareRecursive(astNode[0])
        elif astNode.tag=='BinaryOp':
            code='('+self.declareRecursive(astNode[0])+astNode.get('uid')+self.declareRecursive(astNode[1])+')'
        elif astNode.tag=='Constant':
            code=astNode.get('uid').split(',')[1].strip()
        elif astNode.tag=='ID':
            code=astNode.get('uid')
        elif astNode.tag=='IdentifierType':
            code='sizeof('+astNode.get('uid')+')'
        else:
            for child in astNode:
                code=code+self.declareRecursive(child)
        return code

    def initilizieRecursive(self,astNode):
        code=''
        for child in astNode:
            code=code+'-'+self.initilizieRecursive(child)
        return (astNode.get('uid') if astNode.tag=='ID' else '')+code


    def var_find_size(self, varName, funcName, root):
        # find the size of variabl varName defined in the funcName
        # usefull for dynamic allocation and array definitions
        # NOTICE: currently dynamic allocation is not detected!

        # go through all functions in the code (C/C++ code)
        # find the function which the kernel is called there
        # then find the size of given variable
        if USEPYCPARSER:
            for func in root.findall(".//FuncDef"):
                if self.wrapFuncName(func.find('Decl').get('uid').strip())==funcName.strip():
                    # print('inside '+funcName[cn])
                    funcBody=func.find('Compound')
                    if func.find('.//ParamList'):
                        funcBody.append(func.find('.//ParamList'))
                    for var in funcBody.findall(".//Decl"):
                        # single variable Decl
                        if var.get('uid').split(',')[0].strip()==varName.strip():
                            # print('============ var '+varName+' found')
                            init='unitilialized'
                            if len(var)==2:
                                # print('declaration and initialization')
                                size = self.declareRecursive(var[0])
                                init = self.initilizieRecursive(var[1])
                            elif len(var)==1:
                                #print('only declerations')
                                size = self.declareRecursive(var[0])
                            else:
                                print('unexpected number of children')
                                exit(-1)
                            # check for unknow sizes and dynamic allocations
                            if size.find('unkown')!=-1:
                                print('Error: Unable to determine the array size ('+varName.strip()+')')
                                exit(-1)
                            if size.find('dynamic')!=-1:
                                if DEBUGCP>1:
                                    print('dynamic array detected ('+varName.strip()+')')
                                #exit(-1)
                                # find all assignment expressions and look for allocations
                                # ignore C++ new statements for now
                                #for assignm in funcBody.findall(".//Assignment"):
                                    #if assignm[0].get('uid').strip()==varName.strip():
                                        #allocationSize = assignmentRecursive(assignm)
                            #print('var('+varName+')-> size='+size+' '+'('+init+')')
                            if DEBUGCP>2:
                                print size
                            return size
        else:
            # srcML
            size=srcml_find_var_size(root, funcName, varName)
            if size.find('unkown')!=-1:
                print('Error: Unable to determine the array size ('+varName.strip()+')')
                exit(-1)
            if size.find('dynamic')!=-1:
                if DEBUGCP>1:
                    print('dynamic array detected ('+varName.strip()+')')
            if DEBUGCP>2:
                print size
            if DEBUGSRCMLC:
                print 'Error 1215! unimplemented AST parser!'
            if DEBUGSRCML:
                print 'function:'+funcName+' variable:'+varName+' size:'+size
            if size!='':
                return size
            #exit(-1)
        print('Fatal Internal Error! could not determine the size of variable:'+varName+' in the function:'+funcName+'!')
        exit(-1)

    def var_copy_showAll(self):
        # print detected copy statements to stdout
        for [id, i] in self.oacc_copys:
            print i

    def var_copy_genCode(self):
        # generate proper code for all the copy expressions
        # even generated with data, kernels, or parallel directive
        # and relpace dummy data copy functions with proper allocation and data tansfers

        regex = re.compile(r'([a-zA-Z0-9_]*)([=])(\")([a-zA-Z0-9_:/\+\^\|\&\(\)\*\ \[\]\.>-]*)(\")')
        # explicit memory copies
        for i in range(0,len(self.oacc_copys)):
            codeCin='' #code for performing copyin
            codeCout='' #code for performing copyin
            codeM='' #code for performing allocation
            vardeclare=''
            [kernel_id, cp_expression]=self.oacc_copys[i]
            for j in cp_expression.split('\n'):
                varname=''
                incom=''
                present='false'
                dim=[]
                type=''
                dname=''
                size=''
                parentFunc=''
                clause=''
                dataid=''
                if DEBUGCP>1:
                    print 'Copy tuple > '+j
                for (a, b, c, d, e) in regex.findall(j):
                    if a=='varname':
                        varname=d
                    elif a=='in':
                        incom=d
                    elif a=='present':
                        present=d
                    elif a.find('dim')!=-1:
                        dim.append(d)
                    elif a=='type':
                        type=d
                    elif a=='dname':
                        dname=d
                    elif a=='size':
                        size=d
                    elif a=='parentFunc':
                        parentFunc=d
                    elif a=='clause':
                        clause=d
                    elif a=='dataid':
                        dataid=d
                # handle dynamic allocation here
                if size.find('dynamic')!=-1:
                    if size.count('dynamic')!=len(dim) and not self.oacc_data_dynamicAllowed(clause):
                        print 'Error: [data clause] unable to find a match for variable size! variable name: '+varname+' - clause('+clause+')'
                        exit(-1)
                    for repa in dim:
                        if repa.find(':')==-1:
                            print 'Error: dynamic array without the length at the data clause!'
                            print '\tvariable name: '+varname
                            print '\trange statement: '+repa
                            exit(-1)
                        size=size.replace('dynamic',repa.split(':')[1]+'+'+repa.split(':')[0])
                # duplication check for declaration and allocation
                varmapper_allocated_found=False
                for (pp1, pp2, pp3) in self.varmapper_allocated:
                    if pp1==parentFunc and pp2==dname and pp3==dataid:
                        varmapper_allocated_found=True
                        break
                scalar_copy=(type.count('*')==0)
                ispresent=self.oacc_clauseparser_data_ispresent(clause)
                if varmapper_allocated_found==False:
                    # generate declaration
                    # TODO vardeclare+=self.codegen_devPtrDeclare(type,dname,scalar_copy)+'/* '+dataid+' */\n'
                    # vardeclare+='short '+dname+self.suffix_present+'='+('0')+';\n' # for now we assume are variables are present
                    # generate accelerator allocation
                    if present=='true':
                        # these lines
                        # codeM+='if(!'+dname+self.suffix_present+'){\n'
                        # codeM+=dname+self.suffix_present+'++;\n'
                        # have been replaced with #FIXME
                        #codeM+=dname+'=('+type+')acc_deviceptr((void*)'+('&'if scalar_copy else '')+varname+');\n'
                        codeM+=self.codegen_accDevicePtr(dname,size,varname,type,scalar_copy)
                        codeM+='if('+dname+'==NULL){\n'
                        codeM=codeM+'ipmacc_prompt((char*)"IPMACC: memory allocation '+varname+'\\n");\n'
                        codeM+=self.codegen_memAlloc(dname,size,varname,type,scalar_copy, ispresent)
                        codeM+='}\n'
                        print 'unexpected reach! '
                        exit(-1)
                    elif clause!='present':
                        # this line is removed
                        # codeM+='if(!'+dname+self.suffix_present+'){\n'
                        codeM=codeM+'ipmacc_prompt((char*)"IPMACC: memory allocation '+varname+'\\n");\n'
                        codeM+=self.codegen_memAlloc(dname,size,varname,type,scalar_copy, ispresent)
                        # this line too codeM+='}\n'
                    self.varmapper_allocated.append((parentFunc,dname,dataid))
                # generate memory copy code
                if clause=='copyin' or clause=='copy':
                    codeCin+='ipmacc_prompt((char*)"IPMACC: memory copyin '+varname+'\\n");\n'
                    #codeC+=self.codegen_memCpy(dname, ('&' if scalar_copy else '')+varname, size, 'in')
                    codeCin+=self.codegen_accCopyin(('&' if scalar_copy else '')+varname, dname, size, type, '', scalar_copy )
                if clause=='pcopyin' or clause=='pcopy' or clause=='present_or_copyin' or clause=='present_or_copy':
                    codeCin+='ipmacc_prompt((char*)"IPMACC: memory copyin '+varname+'\\n");\n'
                    codeCin+=self.codegen_accCopyin(('&' if scalar_copy else '')+varname, dname, size, type, 'p', scalar_copy)
                #if clause=='present_or_create':
                #    codeCin+='ipmacc_prompt("IPMACC: memory create or getting device pointer for '+varname+'\\n");\n'
                #    codeCin+=self.codegen_memAlloc(('&' if scalar_copy else '')+varname, dname, size, type)
                if clause=='present':
                    codeCin+='ipmacc_prompt((char*)"IPMACC: memory getting device pointer for '+varname+'\\n");\n'
                    codeCin+=self.codegen_accPresent(('&' if scalar_copy else '')+varname, dname, size, type)
                if clause=='copyout' or clause=='copy' or clause=='pcopyout' or clause=='pcopy' or clause=='present_or_copyout':
                    codeCout+='ipmacc_prompt((char*)"IPMACC: memory copyout '+varname+'\\n");\n'
                    #codeC+=self.codegen_memCpy(('&' if scalar_copy else '')+varname, dname, size, 'out')
                    #codeM+=self.codegen_memAlloc(dname,size,varname,type,scalar_copy, ispresent)
                    codeCout+=self.codegen_accPCopyout(('&' if scalar_copy else '')+varname, dname, size, type, scalar_copy)
            #self.code_include=self.code_include+vardeclare
            self.code=self.code.replace(self.prefix_dataalloc+str(i)+'();',vardeclare+codeM)
            self.code=self.code.replace(self.prefix_datacpin+str(i)+'();',codeCin)
            self.code=self.code.replace(self.prefix_datacpout+str(i)+'();',codeCout)

        # implicit/reduction memory copies
        for i in range(0,len(self.oacc_kernelsImplicit)):
            codeCin='' #code for performing copy in
            codeCout='' #code for performing copy in
            codeM='' #code for performing allocation
            vardeclare=''
            if len(self.oacc_kernelsReductions)!=len(self.oacc_kernelsImplicit):
                print 'Fatal internal error!\n'
                exit(-1)
            for j in (self.oacc_kernelsImplicit[i].split('\n')+self.oacc_kernelsReductions[i].split('\n')):
                varname=''
                incom='inout'
                present='false'
                dim=[]
                type=''
                dname=''
                size=''
                parentFunc=''
                reduc=''
                griddimen=''
                dataid=str(i)
#                regex = re.compile(r'([a-zA-Z0-9_]*)([=])(\")([a-zA-Z0-9_:\(\)\*\ ]*)(\")')
                for (a, b, c, d, e) in regex.findall(j):
                    if a=='varname':
                        varname=d
                    elif a=='present':
                        present=d
                    elif a=='gridDim':
                        griddimen=d
                    elif a.find('dim')!=-1:
                        dim.append(d)
                    elif a=='type':
                        type=d
                    elif a=='dname':
                        dname=d
                    elif a=='size':
                        size=d
                    elif a=='parentFunc':
                        parentFunc=d
                    elif a=='operat':
                        reduc=d
                if varname=='':
                    # invalid tuple, ignore
                    continue
                if DEBUGCP>1:
                    print 'Copy tuple > '+j
                # handle dynamic allocation here
                if size.find('dynamic')!=-1:
                    if size.count('dynamic')!=len(dim):
                        print 'Error: implicit variable cannot be dynamic array! variable name: '+varname
                        print '\tproblem can be avoided by explicit data clause'
                        exit(-1)
                    for repa in dim:
                        if repa.find(':')==-1:
                            print 'Error: dynamic array without the length at the data clause!'
                            print '\tvariable name: '+varname
                            print '\trange statement: '+repa
                            exit(-1)
                        size=size.replace('dynamic',repa.split(':')[1]+'+'+repa.split(':')[0])
                # duplication check for declaration and allocation
                varmapper_allocated_found=False
                dIDs=[]
                dIDs+=self.oacc_kernelsAssociatedCopyIds[i]
                dIDs.reverse()
                for (pp1, pp2, pp3) in self.varmapper_allocated:
                    for did in dIDs:
                        if pp1==parentFunc and pp2==dname and pp3==did:
                            varmapper_allocated_found=True
                            dataid=did
                            break
                    if varmapper_allocated_found:
                        break
                scalar_copy=(type.count('*')==0)
                if varmapper_allocated_found==False:
                    # generate declaration
                    # TODO vardeclare+=self.codegen_devPtrDeclare(type,dname,scalar_copy)+'/* '+dataid+'*/\n'
                    #vardeclare+='short '+dname+self.suffix_present+'='+('0')+';\n' # for now we assume are variables are present
                    # generate accelerator allocation
                    if present=='true':
                        # this lines
                        # codeM+='if(!'+dname+self.suffix_present+'){\n'
                        # codeM+=dname+self.suffix_present+'++;\n'
                        # are replaced with following two lines #FIXME
                        #codeM+=dname+'=('+type+')acc_deviceptr((void*)'+('&'if scalar_copy else '')+varname+');\n'
                        codeM+=self.codegen_accDevicePtr(dname,size,varname,type,scalar_copy)
                        codeM+='if('+dname+'==NULL){\n'
                        codeM=codeM+'ipmacc_prompt((char*)"IPMACC: memory allocation '+varname+'\\n");\n'
                        codeM+=self.codegen_memAlloc(dname,size,varname,type,scalar_copy, False)
                        codeM+='}\n'
                        print 'Unexpected reachment!'
                        exit(-1)
#                    else:
                    self.varmapper_allocated.append((parentFunc,dname,dataid))

                # this line is removed codeM+='if(!'+dname+self.suffix_present+'){\n'
                codeM=codeM+'ipmacc_prompt((char*)"IPMACC: memory allocation '+varname+'\\n");\n'
                #codeM+= self.codegen_memAlloc(dname,size,varname,type,scalar_copy, False)
                if reduc!='':
                    if REDUCTION_TWOLEVELTREE:
                        arrname  = self.prefix_kernel_reduction_array+varname
                        codeM+= type+' '+arrname+'=NULL;\n'
                        #codeM+= 'static '+type+' '+arrname+'=NULL;\n'
                        codeM+= 'if('+arrname+'==NULL){\n'
                        codeM+= arrname+'=('+type+')malloc('+size+');\n'
                        codeM+= self.codegen_memAlloc(dname,size,arrname,type,scalar_copy, False)

                        codeM+= 'for(int __ipmacc_initialize_rv=0; __ipmacc_initialize_rv<'+griddimen+'; __ipmacc_initialize_rv++){\n'
                        if reduc=='min':
                            codeM+=arrname+'[__ipmacc_initialize_rv]= INT_MIN;\n'
                        elif reduc=='max':
                            codeM+=arrname+'[__ipmacc_initialize_rv]= INT_MAX;\n'
                        elif (reduc=='&' or reduc=='&&'):
                            codeM+=arrname+'[__ipmacc_initialize_rv]= 1;\n'
                        else:
                            codeM+=arrname+'[__ipmacc_initialize_rv]= 0;\n'
                        codeM+= '}\n'
                        codeM+= self.codegen_accCopyin(arrname, dname, size, type, 'p',scalar_copy)

                        codeM+= '}\n'
                    else:
                        codeM+= self.codegen_memAlloc(dname,size,varname,type,scalar_copy, False)
                # this line is removed codeM=codeM+'}\n'

                # generate memory copy in/out code
                passbyref='' if reduc=='' else '&'
#                if incom=='true':
                if reduc=='':
                    codeCin+='ipmacc_prompt((char*)"IPMACC: memory copyin '+varname+'\\n");\n'
                    #codeCin+=self.codegen_memCpy(dname, passbyref+varname, size, 'in')
                    codeCin+=self.codegen_accCopyin(passbyref+varname, dname, size, type, 'p', scalar_copy)
                    codeCout+='ipmacc_prompt((char*)"IPMACC: memory copyout '+varname+'\\n");\n'
                    #codeCout+=self.codegen_memCpy(passbyref+varname, dname, size, 'out')
                    codeCout+=self.codegen_accPCopyout(passbyref+varname, dname, size, type, scalar_copy)
                else:
                    if REDUCTION_TWOLEVELTREE:
                        ## allocate host memory
                        #arrname=self.prefix_kernel_reduction_array+varname
                        #codeCin += type+' '+self.prefix_kernel_reduction_array+varname+'=NULL;\n'
                        #codeCin += arrname+'=('+type+')malloc('+size+');\n'
                        codeCout+='ipmacc_prompt((char*)"IPMACC: memory copyout '+varname+'\\n");\n'
                        #codeCout+=self.codegen_memCpy(arrname, dname, size, 'out')
                        codeCout+=self.codegen_accPCopyout(arrname, dname, size, type, scalar_copy)
                        iterator =self.prefix_kernel_reduction_iterator
                        codeCout+='\n/* second-level reduction on '+varname+' */\n'
                        codeCout+='{\n'
                        codeCout+='int '+iterator+'=0;\n'
                        codeCout+='{\n'
                        codeCout+='int bound = '+griddimen+'-1;\n'
                        #codeCout+='int bound = ('++')==0?('+griddimen+'-2):('+griddimen+'-1);\n'
                        codeCout+='for('+iterator+'=bound; '+ iterator+'>0; '+iterator+'-=1){\n'
                        des=arrname+'['+iterator+'-1]'
                        src=arrname+'['+iterator+']'
                        if reduc=='min':
                            codeCout+=des+'=('+(des+'>'+src)+'?'+(src)+':'+(des)+');\n'
                        elif reduc=='max':
                            codeCout+=des+'=('+(des+'>'+src)+'?'+(des)+':'+(src)+');\n'
                        else:
                            codeCout+=des+'='+des+reduc+src+';\n'
                        codeCout+='}\n'
                        codeCout+='}\n'
                        codeCout+='}\n'
                        codeCout+=varname+'='+arrname+'[0];\n'
                        codeCout+='free('+arrname+');\n'

                    else:
                        codeCin +='ipmacc_prompt((char*)"IPMACC: memory copyin '+varname+'\\n");\n'
                        #codeCin +=self.codegen_memCpy(dname, passbyref+varname, size, 'in')
                        codeCin +=self.codegen_accCopyin(passbyref+varname, dname, size, type, 'p', scalar_copy)
                        codeCout+='ipmacc_prompt((char*)"IPMACC: memory copyout '+varname+'\\n");\n'
                        #codeCout+=self.codegen_memCpy(passbyref+varname, dname, size, 'out')
                        codeCout+=self.codegen_accPCopyout(passbyref+varname, dname, size, type, scalar_copy)
                    # reduction do not need copy in for two-level tree
            #self.code_include=self.code_include+vardeclare
            #self.code=self.code.replace(self.prefix_dataalloc+str(i)+'();',vardeclare+codeM)
            self.code=self.code.replace(self.prefix_dataimpli+'in'+str(i)+'();',vardeclare+codeM+codeCin)
            self.code=self.code.replace(self.prefix_dataimpli+'out'+str(i)+'();',codeCout)
   
    
    def var_copy_assignExpDetail(self, forDimOfAllKernels, blockDim):
        # find the type, size, and parentFunction of variables referred in each copy expression
        # and append it to the existing expression

        if USEPYCPARSER:
            text = self.var_parseForYacc(self.code)
            #print text
            # create a pycparser
            parser = c_parser.CParser()
            ast = parser.parse(text, filename='<none>')
            # generate the XML tree
            if DEBUGCP>2:
               ast.show()
            codeAstXml = open('code_ast.xml','w')
            ast.showXml(codeAstXml)
            codeAstXml.close()
            tree = ET.parse('code_ast.xml')
            os.remove('code_ast.xml')
            root = tree.getroot()
        else:
            #srcML
            root=srcml_code2xml(self.code)
            if DEBUGSRCMLC: print 'Error 1498! Unimplemented AST generator!'
            #exit(-1)
             
        # explicit memory copies
        for i in range(0,len(self.oacc_copys)):
            #print i
            [kernel_id, cp_expression]=self.oacc_copys[i]
            list=(cp_expression).split('\n')
            self.oacc_copys[i]=''
            for j in range(0,len(list)-1):
                regex = re.compile(r'([a-zA-Z0-9_]*)([=])(\")([a-zA-Z0-9_:\(\)\*]*)(\")')
                #print 'regex='+regex.findall(list[j])
                for (a, b, c, d, e) in regex.findall(list[j]):
                    if a=='varname':
                            # find the `d` variable in the region
                        try:
                            varNameList=self.oacc_copysVarNams[i]
                            varTypeList=self.oacc_copysVarTyps[i]
                            #print varTypeList[varNameList.index(d)]
                            list[j]=list[j]+' type="'+varTypeList[varNameList.index(d)]+'"'
                            #ndim=varTypeList[varNameList.index(d)].count('*')
                            #for it in range(1,ndim+1):
                            #    list[j]=list[j]+' dim'+str(it)+'="'+'NA'+'"'
                        except:
                            print "fatal error! variable "+d+" is undefined!"
                            print str(len(self.oacc_copysVarNams))+' '+str(len(self.oacc_copys))
                            print "defined  vars: "+','.join(varNameList)
                            print "defined types: "+','.join(varTypeList)
                            exit(-1)
                        list[j]=list[j]+' dname="'+self.varmapper_getDeviceName_elseCreate(self.oacc_copysParent[i],d,[i])+'"'
                        list[j]=list[j]+' size="'+self.var_find_size(d,self.oacc_copysParent[i],root)+'"'
                        list[j]=list[j]+' parentFunc="'+self.oacc_copysParent[i]+'"'
            if DEBUGCP>0:
                print '\n'.join(list[0:len(list)-1])
            self.oacc_copys[i]=[kernel_id, '\n'.join(list[0:len(list)-1])]
            # print self.oacc_copys[i]

        # implicit memory copies
        for i in range(0,len(self.oacc_kernelsImplicit)):
            # implicit
            #print i
            list=self.oacc_kernelsImplicit[i]
            self.oacc_kernelsImplicit[i]=''
            for j in range(0,len(list)):
                if list[j].strip()=='':
                    list[j]=''
                    continue
                d=list[j]
                list[j]='varname="'+d+'"'
                #regex = re.compile(r'([a-zA-Z0-9_]*)([=])(\")([a-zA-Z0-9_:\(\)\*]*)(\")')
                #print 'regex='+regex.findall(list[j])
                try:
                    # find the `d` variable in the region
                    varNameList=self.oacc_kernelsVarNams[i]
                    varTypeList=self.oacc_kernelsVarTyps[i]
                    #print varTypeList[varNameList.index(d)]
                    list[j]=list[j]+' type="'+varTypeList[varNameList.index(d)]+'"'
                except:
                    print "fatal error! implicit variable "+d+" is undefined!"
                    exit(-1)
                list[j]=list[j]+' dname="'+self.varmapper_getDeviceName_elseCreate(self.oacc_kernelsParent[i],d)+'"'
                list[j]=list[j]+' size="'+self.var_find_size(d,self.oacc_kernelsParent[i],root)+'"'
                list[j]=list[j]+' parentFunc="'+self.oacc_kernelsParent[i]+'"'
            if DEBUGCP>0:
                print 'implicit copies for kernel'+str(i)+'> '+('\n'.join(list))
            self.oacc_kernelsImplicit[i]='\n'.join(list)
            # print self.oacc_copys[i]

        # reduction memory copies
        for i in range(0,len(self.oacc_kernelsReductions)):
            list=self.oacc_kernelsReductions[i]
            self.oacc_kernelsReductions[i]=''
            kernelGridDim='('+forDimOfAllKernels[i]+'/'+blockDim+'+1)'
            for j in range(0,len(list)):
                [vnm, init, op, asi, tp]=list[j]
                if vnm.strip()=='':
                    list[j]=''
                    continue
                list[j]='varname="'+vnm+'"'
                list[j]+=' initia="'+init+'"'
                list[j]+=' operat="'+op+'"'
                list[j]+=' assign="'+str(asi)+'"'
#                list[j]+=' predty="'+tp+'"'
                #regex = re.compile(r'([a-zA-Z0-9_]*)([=])(\")([a-zA-Z0-9_:\(\)\*]*)(\")')
                #print 'regex='+regex.findall(list[j])
                try:
                    # find the `vnm` variable in the region
                    varNameList=self.oacc_kernelsVarNams[i]
                    varTypeList=self.oacc_kernelsVarTyps[i]
                    #print varTypeList[varNameList.index(vnm)]
                    list[j]=list[j]+' type="'+varTypeList[varNameList.index(vnm)]+'*"'
                except:
                    print "fatal error! reduction variable "+vnm+" is undefined!"
                    exit(-1)
                list[j]=list[j]+' dname="'+self.varmapper_getDeviceName_elseCreate(self.oacc_kernelsParent[i],vnm,self.oacc_kernelsAssociatedCopyIds[i])+'"'
                list[j]=list[j]+' size="'+((kernelGridDim+'*') if REDUCTION_TWOLEVELTREE else '')+self.var_find_size(vnm,self.oacc_kernelsParent[i],root)+'"'
                list[j]=list[j]+' gridDim="'+kernelGridDim+'"'
                list[j]=list[j]+' parentFunc="'+self.oacc_kernelsParent[i]+'"'
            if DEBUGPRIVRED:
                print 'reduction copies for kernel'+str(i)+'> '+('\n'.join(list))
            self.oacc_kernelsReductions[i]='\n'.join(list)

    # varmapper fuctions
    # handle the mapping between host and device variables
    def varmapper_getDeviceName_elseCreate(self,function,varname, dIDsI=[]):
        # return the deviceName of varname. if does not exist, create one.
        dIDs=dIDsI
        dIDs.reverse()
        for dID in dIDs+[-1]:
            for (a, b, c, d) in self.varmapper:
                if a==function and b==varname and (dID==-1 or dID==c):
                    return d
        dID = -1 if len(dIDs)==0 else dIDs[0]
        dvarname=self.prefix_varmapper+function+'_'+varname+('_'+str(dID) if dID!=-1 else '')
        self.varmapper.append((function, varname, dID, dvarname))
        return dvarname

    def varmapper_getDeviceName(self,function,varname,dIDsI=[]):
        # return the deviceName of varname. if does not exist, create one.
        dIDs=dIDsI
        dIDs.reverse()
        for dID in dIDs+[-1]:
            for (a, b, c, d) in self.varmapper:
                if a==function and b==varname and (dID==-1 or dID==c):
                    return d
        return varname
       
    def varmapper_showAll(self):
        # show all (function, hostVariable) -> deviceVariable mappings
        for (a, b, c, d) in self.varmapper:
            print '('+a+','+b+'.'+c+')->'+d


    def pycparser_getAstTree(self,code):
        text=self.code
        text=text+'int __ipmacc_main(){\n'+code+';\n}'
        text=self.var_parseForYacc(text)
        if DEBUGCPARSER:
            print text
        # handle the error
        if ERRORDUMP:
            f = open('./__ipmacc_c_code_unable_to_parse.c','w')
            old_stdout = sys.stdout
            sys.stdout = f
            print text
            sys.stdout = old_stdout
            f.close()
            sys.stdout = old_stdout
        # create a pycparser
        parser = c_parser.CParser()
        ast = parser.parse(text, filename='<none>')
        if ERRORDUMP:
            os.remove('__ipmacc_c_code_unable_to_parse.c')
        # generate the XML tree
        if DEBUGCPARSER:
            ast.show()
        codeAstXml = open('code_ast.xml','w')
        ast.showXml(codeAstXml)
        codeAstXml.close()
        tree = ET.parse('code_ast.xml')
        os.remove('code_ast.xml')
        root = tree.getroot()
#        return root.find(".//FuncDef/Compound")
        for ch in root.findall(".//FuncDef"):
            #print ch
            if ch.find('Decl').get('uid').strip()=='__ipmacc_main':
                return ch.find('Compound')
        print "Fatal error!"
        exit(-1)
#    def pycparser_getAstTree(self,code):
#        text='int main(){\n'+code+';\n}'
#        if DEBUGCPARSER>0:
#            print text
#        # create a pycparser
#        parser = c_parser.CParser()
#        # handle the dump
#        f = open('./__ipmacc_c_code_unable_to_parse.c','w')
#        old_stdout = sys.stdout
#        sys.stdout = f
#        print text
#        sys.stdout = old_stdout
#        f.close()
#        sys.stdout = old_stdout
#        if ENABLE_INDENT==True:
#            Popen(["indent", filename])

    #
    # VARIABLE TYPE DETECTOR FUNCTIONS: var_kernel_parentsFind, var_copy_parentsFind, var_findFuncParents, var_parseForYacc,
    def astCalcRoot(self):
        if USEPYCPARSER:
            text = self.var_parseForYacc(self.code)
            if DEBUGCPARSER>0:
                print text
            # create a pycparser
            parser = c_parser.CParser()

            # handle the error
            if ERRORDUMP:
                f = open('./__ipmacc_c_code_unable_to_parse.c','w')
                old_stdout = sys.stdout
                sys.stdout = f
                print text
                sys.stdout = old_stdout
                f.close()
                sys.stdout = old_stdout
            ast = parser.parse(text, filename='<none>')
            if ERRORDUMP:
                os.remove('__ipmacc_c_code_unable_to_parse.c')
            
            # generate the XML tree
    #        ast.show()
    #        codeAstXml = open('code_ast.xml','w')
    #        ast.showXml(codeAstXml)
    #        codeAstXml.close()
    #        tree = ET.parse('code_ast.xml')
    #        ast = parser.parse(text, filename='<none>')

            # generate the XML tree
            #ast.show()
            codeAstXml = open('code_ast.xml','w')
            ast.showXml(codeAstXml)
            codeAstXml.close()
            tree = ET.parse('code_ast.xml')
            os.remove('code_ast.xml')
            self.astRoot = tree.getroot()
        else:
            #srcML
            self.astRootML = srcml_code2xml(self.code)
            if DEBUGSRCMLC: print 'Error 1719! Unimplemented AST generator!'
            #exit(-1)

#        root = tree.getroot()
#        return root.find(".//FuncDef/Compound")

#    def astCalcRoot(self):
#        text = self.var_parseForYacc(self.code)
#        if DEBUG>3:
#            print text
#        # create a pycparser
#        parser = c_parser.CParser()
#        ast = parser.parse(text, filename='<none>')
#
#        # generate the XML tree
#        #ast.show()
#        codeAstXml = open('code_ast.xml','w')
#        ast.showXml(codeAstXml)
#        codeAstXml.close()
#        tree = ET.parse('code_ast.xml')
#        os.remove('code_ast.xml')
#        self.astRoot = tree.getroot()



    def oacc_clauseparser_loop_isindependent(self,clause):
        # k=clause.replace('independent','independent()')
        #regex=re.compile(r'([A-Za-z0-9\ ]+)([\(])([A-Za-z0-9\ ]*)([\)])')
        #regex = re.compile(r'([A-Za-z0-9]+)([\ ]*)(\((.+?)\))*')
        indep=False
        private=[]
        reduction=[]
        gang=''
        vector=''
        smc=[]
        #for it in regex.findall(clause):
        for [i0, i3] in clauseDecomposer_break(clause):
            if DEBUGLD:
                print 'clause entry> '+'<>'.join([i0,i3]).strip()
            #if ''.join([i0,i3]).strip()=='independent()':
            # dependent
            if i0.strip()=='independent':
                indep=True
            elif i0.strip()=='seq':
                indep=False
            # private vars
            elif i0.strip()=='private' and i3.strip()!='':
                #private=(i3.strip().replace(',',' ')+' '+private).strip()
                private.append(i3.strip())
            # reduction vars
            elif i0.strip()=='reduction' and i3.strip()!='':
                reduction.append(i3.strip())
            # gang
            elif i0.strip()=='gang' and i3.strip()!='':
                gang=i3.strip()
            # vector
            elif i0.strip()=='vector' and i3.strip()!='':
                vector=i3.strip()
            # smc
            elif i0.strip()=='smc' and i3.strip()!='':
                smc.append(i3.strip())
        if DEBUGLD:
            print 'returning> '+str(indep)+'<>'+','.join(private)+'<>'+','.join(reduction)+'<>'+gang+'<>'+vector
        return [indep, private, reduction, gang, vector, smc]

    def code_gen_reversiFor(self, initial, boundary, increment):
        return 'for('+initial+';'+str(boundary)+';'+str(increment)+')'

    def count_loopIter(self, init, final, operator, steps):
        # initial value of operator
        # final value of operator (in respect to loop condition)
        # operator: the operator of loop iterator increment
        # steps: value of steps for each loop iterator increment
        if operator=='*' or operator=='/':
            return 'log(abs((int)'+final+'-'+init+')'+')'+'/log('+steps+')'
        elif operator=='+' or operator=='-':
            return '(abs((int)'+final+'-'+init+')'+')'+'/('+steps+')'
        else:
            print 'unexpected loop increment operator'
            exit(-1)

    def perform_implicit_copy(self, kernelId, scopeVarsNames, scopeVarsTypes, implicitCopies):
        code_copyin=''
        code_copyout=''
        if DEBUGCP>1:
            print 'Impilict Copy Checking for implicit copy'
        for var in implicitCopies:
            idx=scopeVarsNames.index(var)
            if DEBUGCP>1:
                print '\tretriving information of variable `'+var+'` ('+scopeVarsTypes[idx]+') for implicit copy'
    def oacc_smc_getVarNames(self, kernelId, listOfSmc):
        scopeVarsNames=self.oacc_kernelsVarNams[kernelId]
        scopeVarsTypes=self.oacc_kernelsVarTyps[kernelId]
        endList=[]
        corr=0
        for [kid, vlist] in listOfSmc:
            # each pair corresponds to a call which will be replaced with proper SMC localization
            if kid==kernelId:
                for vop in vlist.split(','):
                    vop=vop.replace(' ','').strip()
                    # find the varname, initvalue,
                    if vop.count(':')!=6:
                        # invalid syntax
                        print 'invalid smc syntax: '+vop
                        print '\t usage: smc(varname[dim1-low:dim1-high:type:pivot:down-range:up-range:divergent])'
                        print '\t note: currently, only one dimension arrays are supported'
                        exit(-1)
                    else:
                        # valid smc
                        spl=vop.split(':')
                        variable=spl[0].split('[')[0]
                        dimlow  =spl[0].split('[')[1]
                        dimhigh =spl[1]
                        smctype =spl[2]
                        pivot   =spl[3]
                        dwrange =spl[4]
                        uprange =spl[5]
                        diverge =spl[6].split(']')[0]
                    # find the type
                    try :
                        idx=scopeVarsNames.index(variable)
                        type=scopeVarsTypes[idx]
                    except:
                        print 'Error: Could not determine the type of variable declared for smc: '+variable
                        exit(-1)
                    endList.append([variable, type, smctype, pivot, dwrange, uprange, diverge, kid, dimlow, dimhigh])
            corr+=1
        return endList

    def oacc_privred_getVarNames(self, kernelId, listOfPrivorRed):
        scopeVarsNames=self.oacc_kernelsVarNams[kernelId]
        scopeVarsTypes=self.oacc_kernelsVarTyps[kernelId]
        endList=[]
        corr=0
        for [kid, vlist] in listOfPrivorRed:
        #for [kid, vlist] in self.oacc_loopReductions:
            # each pair corresponds to a call which will be replaced with proper privatization or reduction
            if kid==kernelId:
                for vop in vlist.split(','):
                    vop=vop.replace(' ','').strip()
                    # find the varname, initvalue,
                    if vop.find(':')==-1:
                        # only privatization
                        #endList.append([vop,'0','U', corr])
                        operation='U'
                        variable=vop
                        initValu='0'
                    else:
                        # privatization and reduction
                        operation=vop.split(':')[0]
                        variable=vop.split(':')[1]
                        initValu='0'
                        if   operation=='+':
                            initValu='0'
                        elif operation=='*':
                            initValu='1'
                        elif operation=='min':
                            initValu='0'
                        elif operation=='max':
                            initValu='0'
                        elif operation=='&':
                            initValu='~0'
                        elif operation=='|':
                            initValu='0'
                        elif operation=='^':
                            initValu='0'
                        elif operation=='&&':
                            initValu='1'
                        elif operation=='||':
                            initValu='0'
                        else:
                            print 'Fatal Error! unexpected reduction operation ('+operation+') on variable '+variable
                            exit(-1)
                    # find the type
                    try :
                        idx=scopeVarsNames.index(variable)
                        type=scopeVarsTypes[idx]
                    except:
                        print 'Error: Could not determine the type of variable declared as private/reduction: '+variable
                        exit(-1)
                    endList.append([variable, initValu, operation, corr, type])
            corr+=1
        return endList

    def find_kernel_undeclaredVars_and_args(self, kernelBody, kernelId):
        # here we look for variable 
        # and return their declarations, if they are not already declared
        # here, conservatively, we define all variables as the function argument
        if USEPYCPARSER:
            root=self.pycparser_getAstTree(kernelBody)
        else:
            #srcML
            root=srcml_code2xml(kernelBody)
            if DEBUGSRCMLC: print 'Error 1862! Unimplemented AST generator!'
            #exit(-1)
        # first find all the function calls IDs
        allFc=[]
        if USEPYCPARSER:
            for fcc in root.findall(".//FuncCall/ID"):
                #allFc.append(str(fcc.get('uid')).strip().replace(',','')) #FIXME
                allFc.append(str(fcc.get('uid')).strip()) 
            allFc=list(set(allFc))
        else:
            #srcML
            allFc=list(srcml_get_fcn_calls(root))
            if DEBUGSRCMLC: print 'Error 1874! Unimplemented AST generator!'
            #exit(-1)
        if VERBOSE==1 and len(allFc)>0:
            print 'kernels region > Function calls: '+','.join(allFc)
        # second, find all the ID tags
        allIds=[]
        if USEPYCPARSER:
            allIds=root.findall(".//ID")
        else:
            #srcML
            if DEBUGCPARSER>0:
                print 'kernel XML > '+tostring(root)
            allIds=srcml_get_all_ids(root)
        if DEBUGCPARSER==1 and len(allIds)>0:
            #print 'identifiers found in the kernels region > : '+', '.join(allIds)
            if DEBUGSRCMLC: print 'Error 1891! Unimplemented AST generator!'
            #exit(-1)
        vars=[]
        for var in allIds:
            if USEPYCPARSER:
                vnm=str(var.get('uid'))
            else:
                vnm=var
            func=True
            try :
                allFc.index(vnm.strip())
            except :
                func=False
            if not func:
                vars.append(vnm.strip())
            else:
                self.active_calls.append(vnm.strip())

        # here we have vars and allFc
        vars=list(set(vars))
        if VERBOSE==1 and len(vars)>0:
            print 'kernels region > Variables: '+', '.join(vars)
        # third, removed defined variables
        vars.remove(self.prefix_kernel_uid);
        if USEPYCPARSER:
            declVarList=root.findall(".//Decl")
        else:
            declVarList=srcml_get_declared_vars(root)
            if DEBUGCPARSER>0:
                print 'declared vars are: > '+','.join(declVarList)
            if DEBUGSRCMLC: print 'Error 1929! Unimplemented AST parser!'
            #exit(-1)
        for var in declVarList:
            try :
                if USEPYCPARSER:
                    vnm=str(var.get('uid'))
                else:
                    vnm=var
                # exclude declared vars
                if DEBUGVAR:
                    print 'variable is defined: '+vnm.strip()
                vars.remove(vnm.strip())
            except :
                # it was a function call, ignore it
                k=True
        if VERBOSE==1 and len(vars)>0:
            print 'kernels region > The variables which aren\'t declared in the region: '+', '.join(vars)
        # fourth, listing all reduction variables of this kernel to:
        # 1) exclude from other copies
        # 2) allocate and transfer final value back to host
        privInfo=self.oacc_privred_getVarNames(kernelId,self.oacc_loopPrivatizin)
        reduInfo=self.oacc_privred_getVarNames(kernelId,self.oacc_loopReductions)
        if DEBUGPRIVRED:
            self.debug_dump_privredInfo('private',privInfo)
            self.debug_dump_privredInfo('reduction',reduInfo)
        # five, listing all smc variables to this kernel
        smcInfo=self.oacc_smc_getVarNames(kernelId,self.oacc_loopSMC)
        if DEBUGSMC:
            self.debug_dump_smcInfo(smcInfo)
        # six, find the function arguments and implicit copies
        scopeVarsNames=self.oacc_kernelsVarNams[kernelId]
        scopeVarsTypes=self.oacc_kernelsVarTyps[kernelId]
        if DEBUGVAR:
            for i in range(0,len(scopeVarsNames)):
                print 'traced var: '+scopeVarsNames[i]+' of '+scopeVarsTypes[i]
        kernelLoopIteratorsPar=self.oacc_kernelsLoopIteratorsPar[kernelId]
        kernelLoopIteratorsSeq=self.oacc_kernelsLoopIteratorsSeq[kernelId]
#        print 'again, kernel iterators > '+','.join(kernelLoopIteratorsPar)
        function_args=[]
        implicitCopies=[]
        for i in range(0,len(vars)):
            # 1- ignore iterator variables (we generate the code later)
#            print 'checking variable > \''+vars[i]+'\''
            itr=True
            try:
                idx=kernelLoopIteratorsPar.index(vars[i].strip())
            except:
                itr=False
            if itr:
                continue
            # 2- check if it is defined as automatic var
            autovar=False
            if len(self.oacc_kernelsAutomaPtrs)>0:
                for av in self.oacc_kernelsAutomaPtrs[kernelId].split(','):
                    if av.strip()==vars[i].strip():
                        autovar=True
                        break
            # 3- check if it is defined as manual var
            manualvar=False
            if len(self.oacc_kernelsManualPtrs) and self.oacc_kernelsManualPtrs[kernelId]!='':
                for mv in self.oacc_kernelsManualPtrs[kernelId].split(','):
                    if mv.strip()==vars[i].strip():
                        manualvar=True
                        break
            # 4- private/reduction variables (exclude from functionArgs for now)
            priv=False # if true, exclude the variable from functionArgs
            redu=False # if true, include a pointer to this variable
            for [priredV, priredI, priredO, corr, typ] in self.unique_priv_list(privInfo+reduInfo):
                if priredV.strip()==vars[i].strip():
                    if priredO=='U':
                        priv=True
                    else:
                        redu=True
                    if DEBUGPRIVRED:
                        print 'varname="'+priredV.strip()+'" is     equal to "'+vars[i].strip()+'"'
                elif DEBUGPRIVRED:
                    print 'varname="'+priredV.strip()+'" is not equal to "'+vars[i].strip()+'"'
            if WARNING and priv and redu:
                print 'warning: the variable is defined both as reduction and private, we assume the reduction (covering private too)'
                priv=False
            # 5- iterators of sequential loops undefined in the region (ignore declaration, we append latter)
            itr=True
            try:
                idx=kernelLoopIteratorsSeq.index(vars[i].strip())
            except:
                itr=False
            if itr:
                continue
            # 6- append function arguments, and find undefined variables (ignore non-pointer)
            undef=False
            pointr=False
            if not priv:
                try :
                    idx=scopeVarsNames.index(vars[i])
                    if scopeVarsTypes[idx].count('*')!=0:
                        # 7- is pointer
                        pointr=True
                    scalar_copy=(scopeVarsTypes[idx].count('*')==0) and manualvar
                    arg_type=scopeVarsTypes[idx]
                    arg_type+='* ' if (redu or scalar_copy) else ' '
                    arg_name=scopeVarsNames[idx]
                    arg_name+=('__ipmacc_scalar' if scalar_copy and (not (redu and manualvar)) else '')
                    arg_name+=('__ipmacc_deviceptr' if autovar else '')
                    arg_name+=('__ipmacc_reductionarray_internal' if redu else '')
                    function_args.append(arg_type+arg_name)
                    #function_args.append(scopeVarsTypes[idx]+('* ' if redu else ' '))
                    #function_args.append(scopeVarsTypes[idx]+('* ' if (redu or not pointr)else ' ')+(scopeVarsNames[idx]+('__ipmacc_scalar' if ((not pointr) and (not redu)) else '')))
                except:
                    if WARNING and not self.iskeyword(vars[i]):
                        print 'warning: Could not determine the type of identifier used in the kernel: '+vars[i]
                        print '\tignoring undefined variable, maybe it\'s a macro or field of struct.'
                        print '\tavailables are: '+','.join(scopeVarsNames)
                    undef=True
                    #exit (-1)
            # 8- track implicit copies
            if WARNING and manualvar and autovar:
                print 'warning: Confusion on declaration of variable `'+vars[i]+'`'
            elif not(undef or manualvar or autovar or (not pointr)):
                # the variable is implicitly defined on device
                # handle the copy-in/copyout
                implicitCopies.append(vars[i].strip())
        # seven, perform implicit copies
        self.perform_implicit_copy(kernelId,scopeVarsNames,scopeVarsTypes,implicitCopies)
        # eight, construct declaration of loop iterators (both parallel and sequential)
        code=''
#        for i in kernelLoopIteratorsPar:
#            code+='int '+i+';\n'
        if DEBUGITER:
            print 'iterators> '+', '.join(kernelLoopIteratorsPar+kernelLoopIteratorsSeq)
        iteratorsList=list(set(kernelLoopIteratorsPar+kernelLoopIteratorsSeq))
        for i in iteratorsList:
            defOutKernel=True
            try :
                idx=scopeVarsNames.index(i)
                code+=scopeVarsTypes[idx]+' '+i+';\n'
            except:
                defOutKernel=False
                if WARNING: print 'warning: Could not determine the type of loop iterator used in the kernel: '+i
            if not defOutKernel:
                # TODO: avoid warning
                # check inside the kernel for the definition 
                # if not exist report error
                if WARNING: print('\tunimplemented fallback')
                #exit(-1)

        # report stats
        if VERBOSE==1:
            if len(function_args)>0: print 'kernels region > kernel arguments: '+', '.join(function_args)
            if len(self.oacc_kernelsAutomaPtrs)>0: print 'kernels region > automatic vars (deviceptr)                 > '+self.oacc_kernelsAutomaPtrs[kernelId]
            if len(self.oacc_kernelsManualPtrs)>0: print 'kernels region > manual    vars (copy in, copy out, create) > '+self.oacc_kernelsManualPtrs[kernelId]
            print 'kernels region > implicit copy peformed for                 > '+','.join(implicitCopies)
        # return function args and early declaration part
        return [function_args, code, implicitCopies, privInfo, reduInfo, smcInfo]

    def kernel_forSize_CReadable(self, list):
        if len(list)==1 and not (type(list[0]) is str):
            return self.kernel_forSize_CReadable(list[0])
        max=[]
        prod=[]
        for ch in list:
            if type(ch) is str:
                prod.append(ch)
            else:
                j=self.kernel_forSize_CReadable(ch)
                if j!='':
                    max.append(j)
        if len(prod)>0 and len(max)>0:
            return '*'.join(prod)+'*'+'IPMACC_MAX'+str(len(max))+'('+','.join(max)+')'
        elif len(prod)>0:
            return '('+'*'.join(prod)+')'
        elif len(max)>0:
            return 'IPMACC_MAX'+str(len(max))+'('+','.join(max)+')'
        else:
            return ''

    def find_kernel_forSize_Recursive(self, root):
        # determining the total reguired threads for parallelism of every loop
        # and marking the lastlevel loop (leaves)
        accumulation=[]
        horizon=[]
        for ch in root:
            t=self.find_kernel_forSize_Recursive(ch)
            if len(t)>0:
                horizon.append(t)
        if len(horizon)>0:
            accumulation.append(horizon)
        if root.tag=='for' and root.attrib['independent']=='true':
            if root.attrib['gang']!='' and root.attrib['vector']!='':
                itercount='('+root.attrib['gang']+'*'+root.attrib['vector']+')'
            else:
                itercount=self.count_loopIter(root.attrib.get('init'),root.attrib.get('terminate'),root.attrib.get('incoperator'),root.attrib.get('incstep'))
            if len(accumulation)==0:
                root.attrib['lastlevel']='true'
                accumulation.append(itercount) #FIXME
                #accumulation.append(root.attrib.get('terminate')) 
                root.attrib['dimloops']=self.kernel_forSize_CReadable(accumulation)
            else:
                root.attrib['lastlevel']='false'
                root.attrib['dimloops']=self.kernel_forSize_CReadable(accumulation)
                accumulation.append(itercount) #FIXME
                #accumulation.append(root.attrib.get('terminate'))
            return accumulation
        else:
            return horizon

    def find_kernel_forSize(self, root):
        iterator_p=[]
        iterator_s=[]
        size=''
        forSize=[]
        for ch in root:
            [it_p, t, it_s]=self.find_kernel_forSize(ch)
            if t!='':
                forSize.append(t)
            if len(it_p)>0:
                iterator_p=iterator_p+it_p
            if len(it_s)>0:
                iterator_s=iterator_s+it_s
        if len(forSize)>0:
            if len(forSize)>1:
                for g in forSize:
                    if g[0]=='@':
                        size=size+g[1:len(g)]+','
                    else:
                        size=size+g+','
                size='<>max('+size[0:len(size)-1]+')'
            else:
                size=('' if (forSize[0][0]=='<' and forSize[0][1]=='>') else '<>')+forSize[0]
        if root.tag=='for' and root.attrib['independent']!='true' and len(root.attrib['initial'].split('=')[0].strip().split(' '))<2:
            # this iterator is undefined, yet non parallel
            iterator_s=iterator_s+[root.attrib.get('iterator')]
        if root.tag=='for' and root.attrib['independent']=='true':
            # append the for size
            iterator_p=iterator_p+[root.attrib.get('iterator')]
            return [iterator_p, '@'+self.count_loopIter(root.attrib.get('init'),root.attrib.get('terminate'),root.attrib.get('incoperator'),root.attrib.get('incstep'))+size, iterator_s]
        return [iterator_p, size, iterator_s]

    def carry_loopAttr2For(self, root, independent, private, reduction, gangs, vectors, smcs):
        # get kernels region and go through to carry loop clauses to the corresponding for
        # mark independent loops, private vars, reduction vars
        if DEBUGLD:
            print 'gang> '+gangs+' vector> '+vectors
        if root.tag=='pragma':
            if root.attrib.get('directive')=='kernels':
                for ch in root:
                    self.carry_loopAttr2For( ch, False, private, reduction, gangs, vectors, smcs)
            elif root.attrib.get('directive')=='loop':
                [indep, priv, reduc, gang, vector, smc]=self.oacc_clauseparser_loop_isindependent(root.attrib.get('clause'))
                for ch in root:
                    self.carry_loopAttr2For(ch, indep, private+priv, reduction+reduc, gangs+gang, vectors+vector, smcs+smc)
            else:
                print('Invalid: '+root.attrib.get('directive')+' directive in region!')
                exit(-1)
        elif root.tag=='for':
            # independent
            if independent:
                root.attrib['independent']='true'
            else :
                root.attrib['independent']='false'
            # cut private
            root.attrib['private']=','.join(private)
            # cut reduction
            root.attrib['reduction']=','.join(reduction)
            # cut gang
            root.attrib['gang']=gangs
            # cut vector
            root.attrib['vector']=vectors
            # cut smc
            root.attrib['smc']=','.join(smcs)
            # go through the childs
            for ch in root:
                self.carry_loopAttr2For(ch, False, [], [], '', '', [])
            if DEBUGLD:
                # print loop attribute
                print self.print_loopAttr(root)

    def var_kernel_genPlainCode(self, id, root, nesting):
        code=''
        try:
            if root.tag=='pragma':
                if root.attrib.get('directive')=='kernels':
                    code=code+'{\n'
                    for ch in root:
                        code=code+self.var_kernel_genPlainCode(id, ch, nesting)
                    code=code+'}\n'
                elif root.attrib.get('directive')=='loop':
                    [indep, priv, reduc, gang, vector, smc]=self.oacc_clauseparser_loop_isindependent(root.attrib.get('clause'))
                    for ch in root:
                        #print str(indep)
                        code=code+self.var_kernel_genPlainCode(id, ch, nesting)
                else:
                    print('Invalid: '+root.attrib.get('directive')+' directive in region!')
                    exit(-1)
            elif root.tag=='for':
                if root.attrib['independent']=='true': #independent:
                    if DEBUGLD:
                        print 'for loop of -> '+root.attrib['iterator']+' -> '+root.attrib['dimloops']
                    # generate indexing
                    if root.attrib['lastlevel']=='true':
                        # last-level
                        if nesting==0:
                            # single parallel loop
                            iteratorVal=(root.attrib.get('init')+root.attrib.get('incoperator'))+'('+self.prefix_kernel_uid+');'
                        else:
                            iteratorVal=(root.attrib.get('init')+root.attrib.get('incoperator'))+'('+self.prefix_kernel_uid+'%('+root.attrib['dimloops']+')'+');'
                    else:
                        # upper levels
                        iteratorVal=(root.attrib.get('init')+root.attrib.get('incoperator'))+'('+self.prefix_kernel_uid+'/('+root.attrib['dimloops']+')'+');'
                    code+=root.attrib.get('declared')+' ' #append iterator type if it is carried
                    code+=root.attrib.get('iterator')+'='+iteratorVal+'\n'
                    # generate work-sharing control statement
                    if root.attrib.get('gang')!='' and root.attrib.get('vector')!='':
                        # FIXME
                        code+='if('+self.prefix_kernel_uid+'<('+root.attrib.get('gang')+'*'+root.attrib.get('vector')+'*'+root.attrib.get('dimloops')+'))'
                        code+='for('+root.attrib.get('iterator')+'='+iteratorVal+' '+root.attrib.get('boundary')+'; '+root.attrib.get('iterator')+'+='+root.attrib.get('gang')+'*'+root.attrib.get('vector')+')\n'
                    else:
                        code+='if('+root.attrib.get('boundary')+')\n'
                    # private/reduction
                    if root.attrib.get('private')!='' or root.attrib.get('reduction')!='':
                        # generate private/reduction declaration
                        separator=(',' if (root.attrib.get('private')!='' and root.attrib.get('reduction')!='') else '')
                        variables=root.attrib.get('private')+separator+root.attrib.get('reduction')
                        code+='{ //opened for private and reduction\n'
                        code=code+'/*private:'+variables+'*/\n'
                        code=code+self.prefix_kernel_privred_region+str(len(self.oacc_loopPrivatizin))+'();'+'\n'
                        self.oacc_loopPrivatizin.append([id,variables])
                    # smc
                    smcId=len(self.oacc_loopSMC)
                    if root.attrib.get('smc')!='' and root.attrib['independent']=='true':
                        code+='{ // opened for smc fetch\n'
                        variables=root.attrib.get('smc')
                        code+=self.prefix_kernel_smc_fetch+str(smcId)+'();\n'
                        self.oacc_loopSMC.append([id,variables])
                    # go through childs
                    for ch in root:
                        code=code+self.var_kernel_genPlainCode(id, ch, nesting+1)
                    if root.attrib.get('smc')!='' and root.attrib['independent']=='true':
                        code+=self.prefix_kernel_smc_fetchend+str(smcId)+'();\n'
                        code+='} // closed for smc fetch end\n'
                    if root.attrib.get('reduction')!='':
                        # generate reduction operations
                        variables=root.attrib.get('reduction')
                        code=code+'/*reduction:'+variables+'*/\n'
                        code=code+self.prefix_kernel_reduction_region+str(len(self.oacc_loopReductions))+'();'+'\n'
                        self.oacc_loopReductions.append([id,variables])
                    if root.attrib.get('private')!='' or root.attrib.get('reduction')!='':
                        code+='} // closed for reduction-end\n'
                    # terminate if statement
                    code=code+'\n'
                else :
                    # generate `for` statement
                    code=code+self.code_gen_reversiFor(root.attrib.get('initial'),root.attrib.get('boundary'),root.attrib.get('increment'))+'\n'
                    # go through childs
                    for ch in root:
                        code=code+self.var_kernel_genPlainCode(id, ch, nesting)
                    # terminate for statement
                    #code=code+root.tag+'\n'
            elif root.tag=='c':
                code=code+root.text.strip()+'\n'
        except Exception as e:
            print 'exception! dumping the code:\n'+self.code+code
            print e
            exit(-1)
        return code

    def debug_dump_privredInfo(self, type, privredList):
        for [v, i, o, a, t] in privredList:
            print type+'> variable: '+v+' initialized: '+i+' operator: '+o+' assignee: '+str(a)+' type: '+t
    def debug_dump_smcInfo(self, smcList):
        for [variable, type, smctype, pivot, dwrange, uprange, diverge, kid, dimlo, dimhi] in smcList:
            print 'SMC info: variable: '+variable+' type: '+type+' smctype: '+smctype+' pivot: '+pivot+' dwrange: '+dwrange+' uprange: '+uprange+' divergent: '+diverge+' assignee: '+str(kid)+' dimlow: '+dimlo+' dimhigh: '+dimhi
    def generate_code(self):
        Argus=[]
        KBody=[]
        Decls=[]
        FDims=[]
        Privs=[]
        Redus=[]
        Smcis=[]
        for i in range(0,len(self.oacc_kernels)):
            if DEBUGLD:
                print 'finding the kernel dimension (`for` size)...'
            [iterators_p, purestring, iterators_s]=self.find_kernel_forSize(self.oacc_kernels[i])
            #print 'it could be something like -> '+str(self.find_kernel_forSize_Recursive(self.oacc_kernels[i]))
            #print 'it could be something like -> '+self.kernel_forSize_CReadable(self.find_kernel_forSize_Recursive(self.oacc_kernels[i]))
            if DEBUGLD or DEBUGVAR:
                 print 'iterators  of parallel   loops :'+','.join(iterators_p)
                 print 'undeclared iterators  of sequential loops :'+','.join(iterators_s)
            iterators_p = list(set(iterators_p))
            self.oacc_kernelsLoopIteratorsPar.append(iterators_p)
            self.oacc_kernelsLoopIteratorsSeq.append(iterators_s)
            forDims=self.kernel_forSize_CReadable(self.find_kernel_forSize_Recursive(self.oacc_kernels[i]))
            if DEBUGLD:
                print 'total concurrent threads -> '+forDims
            kernelBody=self.var_kernel_genPlainCode(i, self.oacc_kernels[i], 0)
            [args, declaration, implicitCopies, privInfo, reduInfo, smcInfo]=self.find_kernel_undeclaredVars_and_args(kernelBody, i)
            self.oacc_kernelsImplicit.append(implicitCopies)
            self.oacc_kernelsReductions.append(list(reduInfo))
            self.oacc_kernelsPrivatizin.append(list(privInfo))
            if DEBUGPRIVRED:
                self.debug_dump_privredInfo('private',privInfo)
                self.debug_dump_privredInfo('reduction',reduInfo)
            # carry the loop break
            Argus.append(args)
            KBody.append(kernelBody)
            Decls.append(declaration)
            FDims.append(forDims)
            Privs.append(privInfo)
            Redus.append(reduInfo)
            Smcis.append(smcInfo)
        
        self.var_copy_assignExpDetail(FDims, (self.blockDim_cuda if self.target_platform=='CUDA' else self.blockDim_opencl))
        self.var_copy_genCode()
        ##k.var_copy_showAll()
        ##k.varmapper_showAll()

        if self.target_platform=='CUDA':
            self.implant_function_prototypes()

        self.forward_declare_find()

        for i in range(0,len(self.oacc_kernels)):
            # carry the loop break
            args=        Argus[i]
            kernelBody=  KBody[i]
            declaration= Decls[i]
            forDims=     FDims[i]
            privInfo=    Privs[i]
            reduInfo=    Redus[i]
            smcInfo=     Smcis[i]
            if DEBUGPRIVRED:
                self.debug_dump_privredInfo('private',privInfo)
                self.debug_dump_privredInfo('reduction',reduInfo)
            # loop continue
            [kernelPrototype, kernelDecl]=self.codegen_constructKernel(args, declaration, kernelBody, i, privInfo, reduInfo, (self.blockDim_cuda if self.target_platform=='CUDA' else self.blockDim_opencl), forDims, smcInfo)
            self.codegen_appendKernelToCode(kernelPrototype, kernelDecl, i, forDims, args, smcInfo)

        if self.target_platform=='OPENCL':
            for k in range(0,len(self.code_kernels)):
                self.code=self.code.replace(self.prefix_kernel+str(k)+'();',self.code_kernels[k])
        if self.target_platform=='CUDA':
            # we can make OpenCL to follow this, however, separating them is easier to debug final code
            #self.code =self.codegen_getFuncProto()  +self.cuda_kernelproto+self.code
            #self.code =self.codegen_getTypeFwrDecl()+self.code
            self.code+=self.codegen_getFuncDecls()  +self.cuda_kerneldecl
            self.codegen_renameStadardTypes()

# check for codegen options
parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="Path to output CU file", metavar="FILE", default="")
#parser.add_option("-t", "--targetarch", dest="target_platform",
#                  help="Target code (nvcuda or nvopencl)", default="")
parser.add_option("-a", "--args", dest="nvcc_args",
                  help="Arguments passed to code generator (mostly, to communicate with underlying gnu cpp)", default="")
(options, args) = parser.parse_args()

#if options.target_platform=="":
#    parser.print_help()
#    exit(-1)

if options.filename=="":
    parser.print_help()
    exit(-1)
#else:
#    print '\twarning: Storing the translated code in <'+options.filename+'> (target: <'+options.target_platform+'>)'

k=codegen('nvcuda',options.filename, options.nvcc_args)
#k=codegen(options.target_platform,options.filename, options.nvcc_args)
filecontent=open(options.filename,'r').readlines()
filecontent=''.join(filecontent)
#for i in filecontent.readlines():
#    print i
#print ''.join(filecontent)
root=srcml_code2xml(filecontent)
k.code_kernelDescendentPrint(root,0)
sk=srcML()
root2=sk.codeToXML(filecontent)
#print sk.getAllText(root2)
arrs=srcml_get_kernelargs(root2)
arrnames=[]
for [arg_name, arg_size, arg_type] in arrs:
    arrnames.append(arg_name)
    #print arg_name

[arraccs,indecis,dependts]=srcml_get_arrayaccesses(root2,arrnames)
# post-process dependencies
#for idx in range(0,len(arraccs)):
#    print 'arrayaccess> '+arraccs[idx]
#    print '\tindecis> '+indecis[idx]
#    for dpv in dependts[idx]:
#        print '\tdepvar> '+dpv

#print k.pycparserGetWritesTo(filecontent)

#'\n'.join(names)

#allIds=srcml_get_kernelargs(root)

