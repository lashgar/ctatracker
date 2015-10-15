/* A Bison parser, made by GNU Bison 2.3.  */

/* Skeleton implementation for Bison's Yacc-like parsers in C

   Copyright (C) 1984, 1989, 1990, 2000, 2001, 2002, 2003, 2004, 2005, 2006
   Free Software Foundation, Inc.

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2, or (at your option)
   any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin Street, Fifth Floor,
   Boston, MA 02110-1301, USA.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* C LALR(1) parser skeleton written by Richard Stallman, by
   simplifying the original so-called "semantic" parser.  */

/* All symbols defined below should begin with yy or YY, to avoid
   infringing on user name space.  This should be done even for local
   variables, as they might otherwise be expanded by user macros.
   There are some unavoidable exceptions within include files to
   define necessary library symbols; they are noted "INFRINGES ON
   USER NAME SPACE" below.  */

/* Identify Bison output.  */
#define YYBISON 1

/* Bison version.  */
#define YYBISON_VERSION "2.3"

/* Skeleton name.  */
#define YYSKELETON_NAME "yacc.c"

/* Pure parsers.  */
#define YYPURE 0

/* Using locations.  */
#define YYLSP_NEEDED 0

/* Substitute the variable and function names.  */
#define yyparse ptx_parse
#define yylex   ptx_lex
#define yyerror ptx_error
#define yylval  ptx_lval
#define yychar  ptx_char
#define yydebug ptx_debug
#define yynerrs ptx_nerrs


/* Tokens.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
   /* Put the tokens into the symbol table, so that GDB and other debuggers
      know about them.  */
   enum yytokentype {
     STRING = 258,
     OPCODE = 259,
     ALIGN_DIRECTIVE = 260,
     BRANCHTARGETS_DIRECTIVE = 261,
     BYTE_DIRECTIVE = 262,
     CALLPROTOTYPE_DIRECTIVE = 263,
     CALLTARGETS_DIRECTIVE = 264,
     CONST_DIRECTIVE = 265,
     CONSTPTR_DIRECTIVE = 266,
     PTR_DIRECTIVE = 267,
     ENTRY_DIRECTIVE = 268,
     EXTERN_DIRECTIVE = 269,
     FILE_DIRECTIVE = 270,
     FUNC_DIRECTIVE = 271,
     GLOBAL_DIRECTIVE = 272,
     LOCAL_DIRECTIVE = 273,
     LOC_DIRECTIVE = 274,
     MAXNCTAPERSM_DIRECTIVE = 275,
     MAXNNREG_DIRECTIVE = 276,
     MAXNTID_DIRECTIVE = 277,
     MINNCTAPERSM_DIRECTIVE = 278,
     PARAM_DIRECTIVE = 279,
     PRAGMA_DIRECTIVE = 280,
     REG_DIRECTIVE = 281,
     REQNTID_DIRECTIVE = 282,
     SECTION_DIRECTIVE = 283,
     SHARED_DIRECTIVE = 284,
     SREG_DIRECTIVE = 285,
     STRUCT_DIRECTIVE = 286,
     SURF_DIRECTIVE = 287,
     TARGET_DIRECTIVE = 288,
     TEX_DIRECTIVE = 289,
     UNION_DIRECTIVE = 290,
     VERSION_DIRECTIVE = 291,
     ADDRESS_SIZE_DIRECTIVE = 292,
     VISIBLE_DIRECTIVE = 293,
     IDENTIFIER = 294,
     INT_OPERAND = 295,
     FLOAT_OPERAND = 296,
     DOUBLE_OPERAND = 297,
     S8_TYPE = 298,
     S16_TYPE = 299,
     S32_TYPE = 300,
     S64_TYPE = 301,
     U8_TYPE = 302,
     U16_TYPE = 303,
     U32_TYPE = 304,
     U64_TYPE = 305,
     F16_TYPE = 306,
     F32_TYPE = 307,
     F64_TYPE = 308,
     FF64_TYPE = 309,
     B8_TYPE = 310,
     B16_TYPE = 311,
     B32_TYPE = 312,
     B64_TYPE = 313,
     BB64_TYPE = 314,
     BB128_TYPE = 315,
     PRED_TYPE = 316,
     TEXREF_TYPE = 317,
     SAMPLERREF_TYPE = 318,
     SURFREF_TYPE = 319,
     V2_TYPE = 320,
     V3_TYPE = 321,
     V4_TYPE = 322,
     COMMA = 323,
     PRED = 324,
     HALF_OPTION = 325,
     EQ_OPTION = 326,
     NE_OPTION = 327,
     LT_OPTION = 328,
     LE_OPTION = 329,
     GT_OPTION = 330,
     GE_OPTION = 331,
     LO_OPTION = 332,
     LS_OPTION = 333,
     HI_OPTION = 334,
     HS_OPTION = 335,
     EQU_OPTION = 336,
     NEU_OPTION = 337,
     LTU_OPTION = 338,
     LEU_OPTION = 339,
     GTU_OPTION = 340,
     GEU_OPTION = 341,
     NUM_OPTION = 342,
     NAN_OPTION = 343,
     CF_OPTION = 344,
     SF_OPTION = 345,
     NSF_OPTION = 346,
     LEFT_SQUARE_BRACKET = 347,
     RIGHT_SQUARE_BRACKET = 348,
     WIDE_OPTION = 349,
     SPECIAL_REGISTER = 350,
     MINUS = 351,
     PLUS = 352,
     COLON = 353,
     SEMI_COLON = 354,
     EXCLAMATION = 355,
     PIPE = 356,
     RIGHT_BRACE = 357,
     LEFT_BRACE = 358,
     EQUALS = 359,
     PERIOD = 360,
     BACKSLASH = 361,
     DIMENSION_MODIFIER = 362,
     RN_OPTION = 363,
     RZ_OPTION = 364,
     RM_OPTION = 365,
     RP_OPTION = 366,
     RNI_OPTION = 367,
     RZI_OPTION = 368,
     RMI_OPTION = 369,
     RPI_OPTION = 370,
     UNI_OPTION = 371,
     GEOM_MODIFIER_1D = 372,
     GEOM_MODIFIER_2D = 373,
     GEOM_MODIFIER_3D = 374,
     SAT_OPTION = 375,
     FTZ_OPTION = 376,
     NEG_OPTION = 377,
     ATOMIC_AND = 378,
     ATOMIC_OR = 379,
     ATOMIC_XOR = 380,
     ATOMIC_CAS = 381,
     ATOMIC_EXCH = 382,
     ATOMIC_ADD = 383,
     ATOMIC_INC = 384,
     ATOMIC_DEC = 385,
     ATOMIC_MIN = 386,
     ATOMIC_MAX = 387,
     LEFT_ANGLE_BRACKET = 388,
     RIGHT_ANGLE_BRACKET = 389,
     LEFT_PAREN = 390,
     RIGHT_PAREN = 391,
     APPROX_OPTION = 392,
     FULL_OPTION = 393,
     ANY_OPTION = 394,
     ALL_OPTION = 395,
     BALLOT_OPTION = 396,
     GLOBAL_OPTION = 397,
     CTA_OPTION = 398,
     SYS_OPTION = 399,
     EXIT_OPTION = 400,
     ABS_OPTION = 401,
     TO_OPTION = 402,
     CA_OPTION = 403,
     CG_OPTION = 404,
     CS_OPTION = 405,
     LU_OPTION = 406,
     CV_OPTION = 407,
     WB_OPTION = 408,
     WT_OPTION = 409
   };
#endif
/* Tokens.  */
#define STRING 258
#define OPCODE 259
#define ALIGN_DIRECTIVE 260
#define BRANCHTARGETS_DIRECTIVE 261
#define BYTE_DIRECTIVE 262
#define CALLPROTOTYPE_DIRECTIVE 263
#define CALLTARGETS_DIRECTIVE 264
#define CONST_DIRECTIVE 265
#define CONSTPTR_DIRECTIVE 266
#define PTR_DIRECTIVE 267
#define ENTRY_DIRECTIVE 268
#define EXTERN_DIRECTIVE 269
#define FILE_DIRECTIVE 270
#define FUNC_DIRECTIVE 271
#define GLOBAL_DIRECTIVE 272
#define LOCAL_DIRECTIVE 273
#define LOC_DIRECTIVE 274
#define MAXNCTAPERSM_DIRECTIVE 275
#define MAXNNREG_DIRECTIVE 276
#define MAXNTID_DIRECTIVE 277
#define MINNCTAPERSM_DIRECTIVE 278
#define PARAM_DIRECTIVE 279
#define PRAGMA_DIRECTIVE 280
#define REG_DIRECTIVE 281
#define REQNTID_DIRECTIVE 282
#define SECTION_DIRECTIVE 283
#define SHARED_DIRECTIVE 284
#define SREG_DIRECTIVE 285
#define STRUCT_DIRECTIVE 286
#define SURF_DIRECTIVE 287
#define TARGET_DIRECTIVE 288
#define TEX_DIRECTIVE 289
#define UNION_DIRECTIVE 290
#define VERSION_DIRECTIVE 291
#define ADDRESS_SIZE_DIRECTIVE 292
#define VISIBLE_DIRECTIVE 293
#define IDENTIFIER 294
#define INT_OPERAND 295
#define FLOAT_OPERAND 296
#define DOUBLE_OPERAND 297
#define S8_TYPE 298
#define S16_TYPE 299
#define S32_TYPE 300
#define S64_TYPE 301
#define U8_TYPE 302
#define U16_TYPE 303
#define U32_TYPE 304
#define U64_TYPE 305
#define F16_TYPE 306
#define F32_TYPE 307
#define F64_TYPE 308
#define FF64_TYPE 309
#define B8_TYPE 310
#define B16_TYPE 311
#define B32_TYPE 312
#define B64_TYPE 313
#define BB64_TYPE 314
#define BB128_TYPE 315
#define PRED_TYPE 316
#define TEXREF_TYPE 317
#define SAMPLERREF_TYPE 318
#define SURFREF_TYPE 319
#define V2_TYPE 320
#define V3_TYPE 321
#define V4_TYPE 322
#define COMMA 323
#define PRED 324
#define HALF_OPTION 325
#define EQ_OPTION 326
#define NE_OPTION 327
#define LT_OPTION 328
#define LE_OPTION 329
#define GT_OPTION 330
#define GE_OPTION 331
#define LO_OPTION 332
#define LS_OPTION 333
#define HI_OPTION 334
#define HS_OPTION 335
#define EQU_OPTION 336
#define NEU_OPTION 337
#define LTU_OPTION 338
#define LEU_OPTION 339
#define GTU_OPTION 340
#define GEU_OPTION 341
#define NUM_OPTION 342
#define NAN_OPTION 343
#define CF_OPTION 344
#define SF_OPTION 345
#define NSF_OPTION 346
#define LEFT_SQUARE_BRACKET 347
#define RIGHT_SQUARE_BRACKET 348
#define WIDE_OPTION 349
#define SPECIAL_REGISTER 350
#define MINUS 351
#define PLUS 352
#define COLON 353
#define SEMI_COLON 354
#define EXCLAMATION 355
#define PIPE 356
#define RIGHT_BRACE 357
#define LEFT_BRACE 358
#define EQUALS 359
#define PERIOD 360
#define BACKSLASH 361
#define DIMENSION_MODIFIER 362
#define RN_OPTION 363
#define RZ_OPTION 364
#define RM_OPTION 365
#define RP_OPTION 366
#define RNI_OPTION 367
#define RZI_OPTION 368
#define RMI_OPTION 369
#define RPI_OPTION 370
#define UNI_OPTION 371
#define GEOM_MODIFIER_1D 372
#define GEOM_MODIFIER_2D 373
#define GEOM_MODIFIER_3D 374
#define SAT_OPTION 375
#define FTZ_OPTION 376
#define NEG_OPTION 377
#define ATOMIC_AND 378
#define ATOMIC_OR 379
#define ATOMIC_XOR 380
#define ATOMIC_CAS 381
#define ATOMIC_EXCH 382
#define ATOMIC_ADD 383
#define ATOMIC_INC 384
#define ATOMIC_DEC 385
#define ATOMIC_MIN 386
#define ATOMIC_MAX 387
#define LEFT_ANGLE_BRACKET 388
#define RIGHT_ANGLE_BRACKET 389
#define LEFT_PAREN 390
#define RIGHT_PAREN 391
#define APPROX_OPTION 392
#define FULL_OPTION 393
#define ANY_OPTION 394
#define ALL_OPTION 395
#define BALLOT_OPTION 396
#define GLOBAL_OPTION 397
#define CTA_OPTION 398
#define SYS_OPTION 399
#define EXIT_OPTION 400
#define ABS_OPTION 401
#define TO_OPTION 402
#define CA_OPTION 403
#define CG_OPTION 404
#define CS_OPTION 405
#define LU_OPTION 406
#define CV_OPTION 407
#define WB_OPTION 408
#define WT_OPTION 409




/* Copy the first part of user declarations.  */


/* Enabling traces.  */
#ifndef YYDEBUG
# define YYDEBUG 1
#endif

/* Enabling verbose error messages.  */
#ifdef YYERROR_VERBOSE
# undef YYERROR_VERBOSE
# define YYERROR_VERBOSE 1
#else
# define YYERROR_VERBOSE 0
#endif

/* Enabling the token table.  */
#ifndef YYTOKEN_TABLE
# define YYTOKEN_TABLE 0
#endif

#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef union YYSTYPE
#line 30 "../src/cuda-sim/ptx.y"
{
  double double_value;
  float  float_value;
  int    int_value;
  char * string_value;
  void * ptr_value;
}
/* Line 193 of yacc.c.  */
#line 421 "ptx.tab.c"
	YYSTYPE;
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
# define YYSTYPE_IS_TRIVIAL 1
#endif



/* Copy the second part of user declarations.  */
#line 194 "../src/cuda-sim/ptx.y"

  	#include "ptx_parser.h"
	#include <stdlib.h>
	#include <string.h>
	#include <math.h>
	void syntax_not_implemented();
	extern int g_func_decl;
	int ptx_lex(void);
	int ptx_error(const char *);


/* Line 216 of yacc.c.  */
#line 444 "ptx.tab.c"

#ifdef short
# undef short
#endif

#ifdef YYTYPE_UINT8
typedef YYTYPE_UINT8 yytype_uint8;
#else
typedef unsigned char yytype_uint8;
#endif

#ifdef YYTYPE_INT8
typedef YYTYPE_INT8 yytype_int8;
#elif (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
typedef signed char yytype_int8;
#else
typedef short int yytype_int8;
#endif

#ifdef YYTYPE_UINT16
typedef YYTYPE_UINT16 yytype_uint16;
#else
typedef unsigned short int yytype_uint16;
#endif

#ifdef YYTYPE_INT16
typedef YYTYPE_INT16 yytype_int16;
#else
typedef short int yytype_int16;
#endif

#ifndef YYSIZE_T
# ifdef __SIZE_TYPE__
#  define YYSIZE_T __SIZE_TYPE__
# elif defined size_t
#  define YYSIZE_T size_t
# elif ! defined YYSIZE_T && (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
#  include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  define YYSIZE_T size_t
# else
#  define YYSIZE_T unsigned int
# endif
#endif

#define YYSIZE_MAXIMUM ((YYSIZE_T) -1)

#ifndef YY_
# if YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> /* INFRINGES ON USER NAME SPACE */
#   define YY_(msgid) dgettext ("bison-runtime", msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(msgid) msgid
# endif
#endif

/* Suppress unused-variable warnings by "using" E.  */
#if ! defined lint || defined __GNUC__
# define YYUSE(e) ((void) (e))
#else
# define YYUSE(e) /* empty */
#endif

/* Identity function, used to suppress warnings about constant conditions.  */
#ifndef lint
# define YYID(n) (n)
#else
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static int
YYID (int i)
#else
static int
YYID (i)
    int i;
#endif
{
  return i;
}
#endif

#if ! defined yyoverflow || YYERROR_VERBOSE

/* The parser invokes alloca or malloc; define the necessary symbols.  */

# ifdef YYSTACK_USE_ALLOCA
#  if YYSTACK_USE_ALLOCA
#   ifdef __GNUC__
#    define YYSTACK_ALLOC __builtin_alloca
#   elif defined __BUILTIN_VA_ARG_INCR
#    include <alloca.h> /* INFRINGES ON USER NAME SPACE */
#   elif defined _AIX
#    define YYSTACK_ALLOC __alloca
#   elif defined _MSC_VER
#    include <malloc.h> /* INFRINGES ON USER NAME SPACE */
#    define alloca _alloca
#   else
#    define YYSTACK_ALLOC alloca
#    if ! defined _ALLOCA_H && ! defined _STDLIB_H && (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
#     include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#     ifndef _STDLIB_H
#      define _STDLIB_H 1
#     endif
#    endif
#   endif
#  endif
# endif

# ifdef YYSTACK_ALLOC
   /* Pacify GCC's `empty if-body' warning.  */
#  define YYSTACK_FREE(Ptr) do { /* empty */; } while (YYID (0))
#  ifndef YYSTACK_ALLOC_MAXIMUM
    /* The OS might guarantee only one guard page at the bottom of the stack,
       and a page size can be as small as 4096 bytes.  So we cannot safely
       invoke alloca (N) if N exceeds 4096.  Use a slightly smaller number
       to allow for a few compiler-allocated temporary stack slots.  */
#   define YYSTACK_ALLOC_MAXIMUM 4032 /* reasonable circa 2006 */
#  endif
# else
#  define YYSTACK_ALLOC YYMALLOC
#  define YYSTACK_FREE YYFREE
#  ifndef YYSTACK_ALLOC_MAXIMUM
#   define YYSTACK_ALLOC_MAXIMUM YYSIZE_MAXIMUM
#  endif
#  if (defined __cplusplus && ! defined _STDLIB_H \
       && ! ((defined YYMALLOC || defined malloc) \
	     && (defined YYFREE || defined free)))
#   include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#   ifndef _STDLIB_H
#    define _STDLIB_H 1
#   endif
#  endif
#  ifndef YYMALLOC
#   define YYMALLOC malloc
#   if ! defined malloc && ! defined _STDLIB_H && (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
void *malloc (YYSIZE_T); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
#  ifndef YYFREE
#   define YYFREE free
#   if ! defined free && ! defined _STDLIB_H && (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
void free (void *); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
# endif
#endif /* ! defined yyoverflow || YYERROR_VERBOSE */


#if (! defined yyoverflow \
     && (! defined __cplusplus \
	 || (defined YYSTYPE_IS_TRIVIAL && YYSTYPE_IS_TRIVIAL)))

/* A type that is properly aligned for any stack member.  */
union yyalloc
{
  yytype_int16 yyss;
  YYSTYPE yyvs;
  };

/* The size of the maximum gap between one aligned stack and the next.  */
# define YYSTACK_GAP_MAXIMUM (sizeof (union yyalloc) - 1)

/* The size of an array large to enough to hold all stacks, each with
   N elements.  */
# define YYSTACK_BYTES(N) \
     ((N) * (sizeof (yytype_int16) + sizeof (YYSTYPE)) \
      + YYSTACK_GAP_MAXIMUM)

/* Copy COUNT objects from FROM to TO.  The source and destination do
   not overlap.  */
# ifndef YYCOPY
#  if defined __GNUC__ && 1 < __GNUC__
#   define YYCOPY(To, From, Count) \
      __builtin_memcpy (To, From, (Count) * sizeof (*(From)))
#  else
#   define YYCOPY(To, From, Count)		\
      do					\
	{					\
	  YYSIZE_T yyi;				\
	  for (yyi = 0; yyi < (Count); yyi++)	\
	    (To)[yyi] = (From)[yyi];		\
	}					\
      while (YYID (0))
#  endif
# endif

/* Relocate STACK from its old location to the new one.  The
   local variables YYSIZE and YYSTACKSIZE give the old and new number of
   elements in the stack, and YYPTR gives the new location of the
   stack.  Advance YYPTR to a properly aligned location for the next
   stack.  */
# define YYSTACK_RELOCATE(Stack)					\
    do									\
      {									\
	YYSIZE_T yynewbytes;						\
	YYCOPY (&yyptr->Stack, Stack, yysize);				\
	Stack = &yyptr->Stack;						\
	yynewbytes = yystacksize * sizeof (*Stack) + YYSTACK_GAP_MAXIMUM; \
	yyptr += yynewbytes / sizeof (*yyptr);				\
      }									\
    while (YYID (0))

#endif

/* YYFINAL -- State number of the termination state.  */
#define YYFINAL  2
/* YYLAST -- Last index in YYTABLE.  */
#define YYLAST   598

/* YYNTOKENS -- Number of terminals.  */
#define YYNTOKENS  155
/* YYNNTS -- Number of nonterminals.  */
#define YYNNTS  64
/* YYNRULES -- Number of rules.  */
#define YYNRULES  268
/* YYNRULES -- Number of states.  */
#define YYNSTATES  374

/* YYTRANSLATE(YYLEX) -- Bison symbol number corresponding to YYLEX.  */
#define YYUNDEFTOK  2
#define YYMAXUTOK   409

#define YYTRANSLATE(YYX)						\
  ((unsigned int) (YYX) <= YYMAXUTOK ? yytranslate[YYX] : YYUNDEFTOK)

/* YYTRANSLATE[YYLEX] -- Bison symbol number corresponding to YYLEX.  */
static const yytype_uint8 yytranslate[] =
{
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      25,    26,    27,    28,    29,    30,    31,    32,    33,    34,
      35,    36,    37,    38,    39,    40,    41,    42,    43,    44,
      45,    46,    47,    48,    49,    50,    51,    52,    53,    54,
      55,    56,    57,    58,    59,    60,    61,    62,    63,    64,
      65,    66,    67,    68,    69,    70,    71,    72,    73,    74,
      75,    76,    77,    78,    79,    80,    81,    82,    83,    84,
      85,    86,    87,    88,    89,    90,    91,    92,    93,    94,
      95,    96,    97,    98,    99,   100,   101,   102,   103,   104,
     105,   106,   107,   108,   109,   110,   111,   112,   113,   114,
     115,   116,   117,   118,   119,   120,   121,   122,   123,   124,
     125,   126,   127,   128,   129,   130,   131,   132,   133,   134,
     135,   136,   137,   138,   139,   140,   141,   142,   143,   144,
     145,   146,   147,   148,   149,   150,   151,   152,   153,   154
};

#if YYDEBUG
/* YYPRHS[YYN] -- Index of the first RHS symbol of rule number YYN in
   YYRHS.  */
static const yytype_uint16 yyprhs[] =
{
       0,     0,     3,     4,     7,    10,    13,    14,    18,    19,
      20,    26,    33,    36,    39,    41,    44,    45,    46,    54,
      55,    59,    61,    62,    63,    70,    72,    74,    76,    79,
      82,    83,    85,    86,    91,    92,    98,    99,   104,   105,
     109,   112,   114,   116,   118,   121,   125,   127,   129,   132,
     135,   138,   140,   143,   146,   150,   153,   158,   165,   168,
     172,   177,   181,   184,   187,   192,   197,   204,   206,   208,
     212,   214,   219,   223,   228,   230,   233,   235,   237,   239,
     241,   244,   246,   248,   250,   252,   254,   256,   258,   260,
     262,   264,   266,   269,   271,   273,   275,   277,   279,   281,
     283,   285,   287,   289,   291,   293,   295,   297,   299,   301,
     303,   305,   307,   309,   311,   313,   315,   317,   319,   323,
     327,   329,   333,   336,   339,   343,   344,   356,   363,   369,
     372,   374,   375,   379,   381,   384,   388,   392,   396,   400,
     404,   408,   412,   416,   420,   424,   428,   432,   434,   437,
     439,   441,   443,   445,   447,   449,   451,   453,   455,   457,
     459,   461,   463,   465,   467,   469,   471,   473,   475,   477,
     479,   481,   483,   485,   487,   489,   491,   493,   495,   497,
     499,   501,   503,   505,   507,   509,   511,   513,   515,   517,
     519,   521,   523,   525,   527,   529,   531,   533,   535,   537,
     539,   541,   543,   545,   547,   549,   551,   553,   555,   557,
     559,   561,   563,   565,   567,   569,   571,   573,   575,   577,
     579,   583,   585,   588,   591,   593,   595,   597,   599,   602,
     604,   608,   611,   615,   618,   622,   626,   631,   636,   640,
     645,   650,   656,   664,   674,   678,   679,   686,   689,   691,
     695,   700,   705,   710,   713,   717,   722,   727,   732,   738,
     744,   749,   751,   753,   755,   757,   760,   763,   767
};

/* YYRHS -- A `-1'-separated list of the rules' RHS.  */
static const yytype_int16 yyrhs[] =
{
     156,     0,    -1,    -1,   156,   181,    -1,   156,   157,    -1,
     156,   163,    -1,    -1,   163,   158,   179,    -1,    -1,    -1,
     163,   159,   162,   160,   179,    -1,    22,    40,    68,    40,
      68,    40,    -1,    23,    40,    -1,    20,    40,    -1,   161,
      -1,   162,   161,    -1,    -1,    -1,   170,   135,   164,   173,
     136,   165,   167,    -1,    -1,   170,   166,   167,    -1,   170,
      -1,    -1,    -1,    39,   168,   135,   169,   171,   136,    -1,
      39,    -1,    13,    -1,    16,    -1,    38,    16,    -1,    14,
      16,    -1,    -1,   173,    -1,    -1,   171,    68,   172,   173,
      -1,    -1,    24,   174,   183,   176,   185,    -1,    -1,    26,
     175,   183,   185,    -1,    -1,    12,   177,   178,    -1,    12,
     178,    -1,    17,    -1,    18,    -1,    29,    -1,     5,    40,
      -1,   103,   180,   102,    -1,   181,    -1,   196,    -1,   180,
     181,    -1,   180,   196,    -1,   180,   179,    -1,   179,    -1,
     182,    99,    -1,    36,    42,    -1,    36,    42,    97,    -1,
      37,    40,    -1,    33,    39,    68,    39,    -1,    33,    39,
      68,    39,    68,    39,    -1,    33,    39,    -1,    15,    40,
       3,    -1,    19,    40,    40,    40,    -1,    25,     3,    99,
      -1,   163,    99,    -1,   183,   184,    -1,   183,   185,   104,
     194,    -1,   183,   185,   104,   217,    -1,    11,    39,    68,
      39,    68,    40,    -1,   186,    -1,   185,    -1,   184,    68,
     185,    -1,    39,    -1,    39,   133,    40,   134,    -1,    39,
      92,    93,    -1,    39,    92,    40,    93,    -1,   187,    -1,
     186,   187,    -1,   189,    -1,   191,    -1,   188,    -1,    14,
      -1,     5,    40,    -1,    26,    -1,    30,    -1,   190,    -1,
      10,    -1,    17,    -1,    18,    -1,    24,    -1,    29,    -1,
      32,    -1,    34,    -1,   193,    -1,   192,   193,    -1,    65,
      -1,    66,    -1,    67,    -1,    43,    -1,    44,    -1,    45,
      -1,    46,    -1,    47,    -1,    48,    -1,    49,    -1,    50,
      -1,    51,    -1,    52,    -1,    53,    -1,    54,    -1,    55,
      -1,    56,    -1,    57,    -1,    58,    -1,    59,    -1,    60,
      -1,    61,    -1,    62,    -1,    63,    -1,    64,    -1,   103,
     195,   102,    -1,   103,   194,   102,    -1,   217,    -1,   195,
      68,   217,    -1,   197,    99,    -1,    39,    98,    -1,   201,
     197,    99,    -1,    -1,   199,   135,   210,   136,   198,    68,
     210,    68,   135,   209,   136,    -1,   199,   210,    68,   135,
     209,   136,    -1,   199,   210,    68,   135,   136,    -1,   199,
     209,    -1,   199,    -1,    -1,     4,   200,   202,    -1,     4,
      -1,    69,    39,    -1,    69,   100,    39,    -1,    69,    39,
      73,    -1,    69,    39,    71,    -1,    69,    39,    74,    -1,
      69,    39,    72,    -1,    69,    39,    76,    -1,    69,    39,
      81,    -1,    69,    39,    85,    -1,    69,    39,    82,    -1,
      69,    39,    89,    -1,    69,    39,    90,    -1,    69,    39,
      91,    -1,   203,    -1,   203,   202,    -1,   191,    -1,   208,
      -1,   190,    -1,   205,    -1,   116,    -1,    94,    -1,   139,
      -1,   140,    -1,   141,    -1,   142,    -1,   143,    -1,   144,
      -1,   117,    -1,   118,    -1,   119,    -1,   120,    -1,   121,
      -1,   122,    -1,   137,    -1,   138,    -1,   145,    -1,   146,
      -1,   204,    -1,   147,    -1,    70,    -1,   148,    -1,   149,
      -1,   150,    -1,   151,    -1,   152,    -1,   153,    -1,   154,
      -1,   123,    -1,   124,    -1,   125,    -1,   126,    -1,   127,
      -1,   128,    -1,   129,    -1,   130,    -1,   131,    -1,   132,
      -1,   206,    -1,   207,    -1,   108,    -1,   109,    -1,   110,
      -1,   111,    -1,   112,    -1,   113,    -1,   114,    -1,   115,
      -1,    71,    -1,    72,    -1,    73,    -1,    74,    -1,    75,
      -1,    76,    -1,    77,    -1,    78,    -1,    79,    -1,    80,
      -1,    81,    -1,    82,    -1,    83,    -1,    84,    -1,    85,
      -1,    86,    -1,    87,    -1,    88,    -1,   210,    -1,   210,
      68,   209,    -1,    39,    -1,   100,    39,    -1,    96,    39,
      -1,   215,    -1,   217,    -1,   214,    -1,   211,    -1,    96,
     211,    -1,   212,    -1,    39,    97,    40,    -1,    39,    77,
      -1,    96,    39,    77,    -1,    39,    79,    -1,    96,    39,
      79,    -1,    39,   101,    39,    -1,    39,   101,    39,    77,
      -1,    39,   101,    39,    79,    -1,    39,   106,    39,    -1,
      39,   106,    39,    77,    -1,    39,   106,    39,    79,    -1,
     103,    39,    68,    39,   102,    -1,   103,    39,    68,    39,
      68,    39,   102,    -1,   103,    39,    68,    39,    68,    39,
      68,    39,   102,    -1,   103,    39,   102,    -1,    -1,    92,
      39,    68,   213,   211,    93,    -1,    95,   107,    -1,    95,
      -1,    92,   218,    93,    -1,    39,    92,   218,    93,    -1,
      39,    92,   217,    93,    -1,    39,    92,   216,    93,    -1,
      96,   215,    -1,    39,    97,    39,    -1,    39,    97,    39,
      77,    -1,    39,    97,    39,    79,    -1,    39,    97,   104,
      39,    -1,    39,    97,   104,    39,    77,    -1,    39,    97,
     104,    39,    79,    -1,    39,    97,   104,    40,    -1,    40,
      -1,    41,    -1,    42,    -1,    39,    -1,    39,    77,    -1,
      39,    79,    -1,    39,    97,    40,    -1,    40,    -1
};

/* YYRLINE[YYN] -- source line where rule number YYN was defined.  */
static const yytype_uint16 yyrline[] =
{
       0,   207,   207,   208,   209,   210,   213,   213,   214,   214,
     214,   217,   220,   221,   224,   225,   228,   228,   228,   229,
     229,   230,   233,   233,   233,   234,   237,   238,   239,   240,
     243,   244,   245,   245,   247,   247,   248,   248,   250,   251,
     252,   254,   255,   256,   258,   260,   262,   263,   264,   265,
     266,   267,   270,   271,   272,   273,   274,   275,   276,   277,
     278,   279,   280,   283,   284,   285,   286,   289,   291,   292,
     294,   295,   307,   308,   311,   312,   314,   315,   316,   317,
     320,   322,   323,   324,   327,   328,   329,   330,   331,   332,
     333,   336,   337,   340,   341,   342,   345,   346,   347,   348,
     349,   350,   351,   352,   353,   354,   355,   356,   357,   358,
     359,   360,   361,   362,   363,   364,   365,   366,   369,   370,
     372,   373,   375,   376,   377,   379,   379,   380,   381,   382,
     383,   386,   386,   387,   389,   390,   391,   392,   393,   394,
     395,   396,   397,   398,   399,   400,   401,   404,   405,   407,
     408,   409,   410,   411,   412,   413,   414,   415,   416,   417,
     418,   419,   420,   421,   422,   423,   424,   425,   426,   427,
     428,   429,   430,   431,   432,   433,   434,   435,   436,   437,
     438,   441,   442,   443,   444,   445,   446,   447,   448,   449,
     450,   453,   454,   456,   457,   458,   459,   462,   463,   464,
     465,   468,   469,   470,   471,   472,   473,   474,   475,   476,
     477,   478,   479,   480,   481,   482,   483,   484,   485,   488,
     489,   491,   492,   493,   494,   495,   496,   497,   498,   499,
     500,   501,   502,   503,   504,   505,   506,   507,   508,   509,
     510,   513,   514,   515,   516,   519,   519,   524,   525,   528,
     529,   530,   531,   532,   535,   536,   537,   538,   539,   540,
     541,   544,   545,   546,   549,   550,   551,   552,   553
};
#endif

#if YYDEBUG || YYERROR_VERBOSE || YYTOKEN_TABLE
/* YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
   First, the terminals, then, starting at YYNTOKENS, nonterminals.  */
static const char *const yytname[] =
{
  "$end", "error", "$undefined", "STRING", "OPCODE", "ALIGN_DIRECTIVE",
  "BRANCHTARGETS_DIRECTIVE", "BYTE_DIRECTIVE", "CALLPROTOTYPE_DIRECTIVE",
  "CALLTARGETS_DIRECTIVE", "CONST_DIRECTIVE", "CONSTPTR_DIRECTIVE",
  "PTR_DIRECTIVE", "ENTRY_DIRECTIVE", "EXTERN_DIRECTIVE", "FILE_DIRECTIVE",
  "FUNC_DIRECTIVE", "GLOBAL_DIRECTIVE", "LOCAL_DIRECTIVE", "LOC_DIRECTIVE",
  "MAXNCTAPERSM_DIRECTIVE", "MAXNNREG_DIRECTIVE", "MAXNTID_DIRECTIVE",
  "MINNCTAPERSM_DIRECTIVE", "PARAM_DIRECTIVE", "PRAGMA_DIRECTIVE",
  "REG_DIRECTIVE", "REQNTID_DIRECTIVE", "SECTION_DIRECTIVE",
  "SHARED_DIRECTIVE", "SREG_DIRECTIVE", "STRUCT_DIRECTIVE",
  "SURF_DIRECTIVE", "TARGET_DIRECTIVE", "TEX_DIRECTIVE", "UNION_DIRECTIVE",
  "VERSION_DIRECTIVE", "ADDRESS_SIZE_DIRECTIVE", "VISIBLE_DIRECTIVE",
  "IDENTIFIER", "INT_OPERAND", "FLOAT_OPERAND", "DOUBLE_OPERAND",
  "S8_TYPE", "S16_TYPE", "S32_TYPE", "S64_TYPE", "U8_TYPE", "U16_TYPE",
  "U32_TYPE", "U64_TYPE", "F16_TYPE", "F32_TYPE", "F64_TYPE", "FF64_TYPE",
  "B8_TYPE", "B16_TYPE", "B32_TYPE", "B64_TYPE", "BB64_TYPE", "BB128_TYPE",
  "PRED_TYPE", "TEXREF_TYPE", "SAMPLERREF_TYPE", "SURFREF_TYPE", "V2_TYPE",
  "V3_TYPE", "V4_TYPE", "COMMA", "PRED", "HALF_OPTION", "EQ_OPTION",
  "NE_OPTION", "LT_OPTION", "LE_OPTION", "GT_OPTION", "GE_OPTION",
  "LO_OPTION", "LS_OPTION", "HI_OPTION", "HS_OPTION", "EQU_OPTION",
  "NEU_OPTION", "LTU_OPTION", "LEU_OPTION", "GTU_OPTION", "GEU_OPTION",
  "NUM_OPTION", "NAN_OPTION", "CF_OPTION", "SF_OPTION", "NSF_OPTION",
  "LEFT_SQUARE_BRACKET", "RIGHT_SQUARE_BRACKET", "WIDE_OPTION",
  "SPECIAL_REGISTER", "MINUS", "PLUS", "COLON", "SEMI_COLON",
  "EXCLAMATION", "PIPE", "RIGHT_BRACE", "LEFT_BRACE", "EQUALS", "PERIOD",
  "BACKSLASH", "DIMENSION_MODIFIER", "RN_OPTION", "RZ_OPTION", "RM_OPTION",
  "RP_OPTION", "RNI_OPTION", "RZI_OPTION", "RMI_OPTION", "RPI_OPTION",
  "UNI_OPTION", "GEOM_MODIFIER_1D", "GEOM_MODIFIER_2D", "GEOM_MODIFIER_3D",
  "SAT_OPTION", "FTZ_OPTION", "NEG_OPTION", "ATOMIC_AND", "ATOMIC_OR",
  "ATOMIC_XOR", "ATOMIC_CAS", "ATOMIC_EXCH", "ATOMIC_ADD", "ATOMIC_INC",
  "ATOMIC_DEC", "ATOMIC_MIN", "ATOMIC_MAX", "LEFT_ANGLE_BRACKET",
  "RIGHT_ANGLE_BRACKET", "LEFT_PAREN", "RIGHT_PAREN", "APPROX_OPTION",
  "FULL_OPTION", "ANY_OPTION", "ALL_OPTION", "BALLOT_OPTION",
  "GLOBAL_OPTION", "CTA_OPTION", "SYS_OPTION", "EXIT_OPTION", "ABS_OPTION",
  "TO_OPTION", "CA_OPTION", "CG_OPTION", "CS_OPTION", "LU_OPTION",
  "CV_OPTION", "WB_OPTION", "WT_OPTION", "$accept", "input",
  "function_defn", "@1", "@2", "@3", "block_spec", "block_spec_list",
  "function_decl", "@4", "@5", "@6", "function_ident_param", "@7", "@8",
  "function_decl_header", "param_list", "@9", "param_entry", "@10", "@11",
  "ptr_spec", "ptr_space_spec", "ptr_align_spec", "statement_block",
  "statement_list", "directive_statement", "variable_declaration",
  "variable_spec", "identifier_list", "identifier_spec", "var_spec_list",
  "var_spec", "align_spec", "space_spec", "addressable_spec", "type_spec",
  "vector_spec", "scalar_type", "initializer_list", "literal_list",
  "instruction_statement", "instruction", "@12", "opcode_spec", "@13",
  "pred_spec", "option_list", "option", "atomic_operation_spec",
  "rounding_mode", "floating_point_rounding_mode", "integer_rounding_mode",
  "compare_spec", "operand_list", "operand", "vector_operand",
  "tex_operand", "@14", "builtin_operand", "memory_operand",
  "twin_operand", "literal_operand", "address_expression", 0
};
#endif

# ifdef YYPRINT
/* YYTOKNUM[YYLEX-NUM] -- Internal token number corresponding to
   token YYLEX-NUM.  */
static const yytype_uint16 yytoknum[] =
{
       0,   256,   257,   258,   259,   260,   261,   262,   263,   264,
     265,   266,   267,   268,   269,   270,   271,   272,   273,   274,
     275,   276,   277,   278,   279,   280,   281,   282,   283,   284,
     285,   286,   287,   288,   289,   290,   291,   292,   293,   294,
     295,   296,   297,   298,   299,   300,   301,   302,   303,   304,
     305,   306,   307,   308,   309,   310,   311,   312,   313,   314,
     315,   316,   317,   318,   319,   320,   321,   322,   323,   324,
     325,   326,   327,   328,   329,   330,   331,   332,   333,   334,
     335,   336,   337,   338,   339,   340,   341,   342,   343,   344,
     345,   346,   347,   348,   349,   350,   351,   352,   353,   354,
     355,   356,   357,   358,   359,   360,   361,   362,   363,   364,
     365,   366,   367,   368,   369,   370,   371,   372,   373,   374,
     375,   376,   377,   378,   379,   380,   381,   382,   383,   384,
     385,   386,   387,   388,   389,   390,   391,   392,   393,   394,
     395,   396,   397,   398,   399,   400,   401,   402,   403,   404,
     405,   406,   407,   408,   409
};
# endif

/* YYR1[YYN] -- Symbol number of symbol that rule YYN derives.  */
static const yytype_uint8 yyr1[] =
{
       0,   155,   156,   156,   156,   156,   158,   157,   159,   160,
     157,   161,   161,   161,   162,   162,   164,   165,   163,   166,
     163,   163,   168,   169,   167,   167,   170,   170,   170,   170,
     171,   171,   172,   171,   174,   173,   175,   173,   176,   176,
     176,   177,   177,   177,   178,   179,   180,   180,   180,   180,
     180,   180,   181,   181,   181,   181,   181,   181,   181,   181,
     181,   181,   181,   182,   182,   182,   182,   183,   184,   184,
     185,   185,   185,   185,   186,   186,   187,   187,   187,   187,
     188,   189,   189,   189,   190,   190,   190,   190,   190,   190,
     190,   191,   191,   192,   192,   192,   193,   193,   193,   193,
     193,   193,   193,   193,   193,   193,   193,   193,   193,   193,
     193,   193,   193,   193,   193,   193,   193,   193,   194,   194,
     195,   195,   196,   196,   196,   198,   197,   197,   197,   197,
     197,   200,   199,   199,   201,   201,   201,   201,   201,   201,
     201,   201,   201,   201,   201,   201,   201,   202,   202,   203,
     203,   203,   203,   203,   203,   203,   203,   203,   203,   203,
     203,   203,   203,   203,   203,   203,   203,   203,   203,   203,
     203,   203,   203,   203,   203,   203,   203,   203,   203,   203,
     203,   204,   204,   204,   204,   204,   204,   204,   204,   204,
     204,   205,   205,   206,   206,   206,   206,   207,   207,   207,
     207,   208,   208,   208,   208,   208,   208,   208,   208,   208,
     208,   208,   208,   208,   208,   208,   208,   208,   208,   209,
     209,   210,   210,   210,   210,   210,   210,   210,   210,   210,
     210,   210,   210,   210,   210,   210,   210,   210,   210,   210,
     210,   211,   211,   211,   211,   213,   212,   214,   214,   215,
     215,   215,   215,   215,   216,   216,   216,   216,   216,   216,
     216,   217,   217,   217,   218,   218,   218,   218,   218
};

/* YYR2[YYN] -- Number of symbols composing right hand side of rule YYN.  */
static const yytype_uint8 yyr2[] =
{
       0,     2,     0,     2,     2,     2,     0,     3,     0,     0,
       5,     6,     2,     2,     1,     2,     0,     0,     7,     0,
       3,     1,     0,     0,     6,     1,     1,     1,     2,     2,
       0,     1,     0,     4,     0,     5,     0,     4,     0,     3,
       2,     1,     1,     1,     2,     3,     1,     1,     2,     2,
       2,     1,     2,     2,     3,     2,     4,     6,     2,     3,
       4,     3,     2,     2,     4,     4,     6,     1,     1,     3,
       1,     4,     3,     4,     1,     2,     1,     1,     1,     1,
       2,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     2,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     1,     1,     1,     1,     3,     3,
       1,     3,     2,     2,     3,     0,    11,     6,     5,     2,
       1,     0,     3,     1,     2,     3,     3,     3,     3,     3,
       3,     3,     3,     3,     3,     3,     3,     1,     2,     1,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       3,     1,     2,     2,     1,     1,     1,     1,     2,     1,
       3,     2,     3,     2,     3,     3,     4,     4,     3,     4,
       4,     5,     7,     9,     3,     0,     6,     2,     1,     3,
       4,     4,     4,     2,     3,     4,     4,     4,     5,     5,
       4,     1,     1,     1,     1,     2,     2,     3,     1
};

/* YYDEFACT[STATE-NAME] -- Default rule to reduce with in state
   STATE-NUM when YYTABLE doesn't specify something else to do.  Zero
   means the default is an error.  */
static const yytype_uint16 yydefact[] =
{
       2,     0,     1,     0,    84,     0,    26,    79,     0,    27,
      85,    86,     0,    87,     0,    81,    88,    82,    89,     0,
      90,     0,     0,     0,    96,    97,    98,    99,   100,   101,
     102,   103,   104,   105,   106,   107,   108,   109,   110,   111,
     112,   113,   114,   115,   116,   117,    93,    94,    95,     4,
       5,    21,     3,     0,     0,    67,    74,    78,    76,    83,
      77,     0,    91,    80,     0,    29,     0,     0,     0,    58,
      53,    55,    28,    62,     0,     0,    16,     0,    52,    70,
      63,    68,    79,    75,    92,     0,    59,     0,    61,     0,
      54,     0,     7,     0,     0,     0,    14,     9,     0,    25,
      20,     0,     0,     0,     0,     0,    60,    56,   131,     0,
       0,     0,    51,     0,    46,    47,     0,   130,     0,    13,
       0,    12,     0,    15,    34,    36,     0,     0,     0,    72,
       0,    69,   261,   262,   263,     0,    64,    65,     0,     0,
       0,   123,   134,     0,    45,    50,    48,    49,   122,   221,
       0,   248,     0,     0,     0,     0,   129,   219,   227,   229,
     226,   224,   225,     0,     0,    10,     0,     0,    17,    23,
      73,    71,     0,     0,   120,    66,    57,   173,   201,   202,
     203,   204,   205,   206,   207,   208,   209,   210,   211,   212,
     213,   214,   215,   216,   217,   218,   154,   193,   194,   195,
     196,   197,   198,   199,   200,   153,   161,   162,   163,   164,
     165,   166,   181,   182,   183,   184,   185,   186,   187,   188,
     189,   190,   167,   168,   155,   156,   157,   158,   159,   160,
     169,   170,   172,   174,   175,   176,   177,   178,   179,   180,
     151,   149,   132,   147,   171,   152,   191,   192,   150,   137,
     139,   136,   138,   140,   141,   143,   142,   144,   145,   146,
     135,   231,   233,     0,     0,     0,     0,   264,   268,     0,
     247,   223,     0,     0,   228,   253,   222,     0,     0,     0,
     124,     0,    38,     0,     0,    30,   119,     0,   118,   148,
     264,   261,     0,     0,     0,   230,   235,   238,   245,   265,
     266,     0,   249,   232,   234,   264,     0,     0,   244,   125,
       0,   220,   219,     0,     0,     0,    37,    18,     0,    31,
     121,     0,   252,   251,   250,   236,   237,   239,   240,     0,
     267,     0,     0,   128,     0,     0,    11,     0,    41,    42,
      43,     0,    40,    35,    32,    24,   254,     0,     0,     0,
     241,     0,   127,    44,    39,     0,   255,   256,   257,   260,
     246,     0,     0,    33,   258,   259,     0,   242,     0,     0,
       0,   243,     0,   126
};

/* YYDEFGOTO[NTERM-NUM].  */
static const yytype_int16 yydefgoto[] =
{
      -1,     1,    49,    74,    75,   122,    96,    97,   111,    98,
     284,    77,   100,   127,   285,    51,   318,   355,   126,   166,
     167,   315,   341,   342,    92,   113,    52,    53,    54,    80,
      81,    55,    56,    57,    58,    59,    60,    61,    62,   136,
     173,   115,   116,   332,   117,   140,   118,   242,   243,   244,
     245,   246,   247,   248,   311,   312,   158,   159,   329,   160,
     161,   292,   162,   269
};

/* YYPACT[STATE-NUM] -- Index in YYTABLE of the portion describing
   STATE-NUM.  */
#define YYPACT_NINF -270
static const yytype_int16 yypact[] =
{
    -270,   446,  -270,   -29,  -270,   -33,  -270,     6,   -23,  -270,
    -270,  -270,    -4,  -270,    89,  -270,  -270,  -270,  -270,    26,
    -270,   125,   129,   163,  -270,  -270,  -270,  -270,  -270,  -270,
    -270,  -270,  -270,  -270,  -270,  -270,  -270,  -270,  -270,  -270,
    -270,  -270,  -270,  -270,  -270,  -270,  -270,  -270,  -270,  -270,
     -10,   -31,  -270,    99,   170,   509,  -270,  -270,  -270,  -270,
    -270,   534,  -270,  -270,   144,  -270,   217,   175,   148,   156,
     146,  -270,  -270,  -270,   130,   184,  -270,   213,  -270,    62,
     186,   176,  -270,  -270,  -270,   247,  -270,   248,  -270,   250,
    -270,   287,  -270,   253,   254,   255,  -270,   184,     1,   152,
    -270,    59,   256,   170,    -8,   222,  -270,   231,   268,   220,
     -34,   223,  -270,   212,  -270,  -270,   228,   333,   324,  -270,
     261,  -270,   130,  -270,  -270,  -270,   219,   224,   264,  -270,
     227,  -270,  -270,  -270,  -270,    -8,  -270,  -270,   318,   323,
      -3,  -270,   325,   326,  -270,  -270,  -270,  -270,  -270,   312,
     136,   259,    93,   330,   331,   345,  -270,   308,  -270,  -270,
    -270,  -270,  -270,   278,   342,  -270,   509,   509,  -270,  -270,
    -270,  -270,   281,    90,  -270,  -270,  -270,  -270,  -270,  -270,
    -270,  -270,  -270,  -270,  -270,  -270,  -270,  -270,  -270,  -270,
    -270,  -270,  -270,  -270,  -270,  -270,  -270,  -270,  -270,  -270,
    -270,  -270,  -270,  -270,  -270,  -270,  -270,  -270,  -270,  -270,
    -270,  -270,  -270,  -270,  -270,  -270,  -270,  -270,  -270,  -270,
    -270,  -270,  -270,  -270,  -270,  -270,  -270,  -270,  -270,  -270,
    -270,  -270,  -270,  -270,  -270,  -270,  -270,  -270,  -270,  -270,
    -270,  -270,  -270,    -3,  -270,  -270,  -270,  -270,  -270,  -270,
    -270,  -270,  -270,  -270,  -270,  -270,  -270,  -270,  -270,  -270,
    -270,  -270,  -270,   132,   348,   353,   354,    91,  -270,   301,
    -270,   126,   200,    -2,  -270,  -270,  -270,    92,   266,   339,
    -270,   327,   388,   170,   213,     1,  -270,    56,  -270,  -270,
     -59,  -270,   315,   319,   328,  -270,   131,   134,  -270,  -270,
    -270,   365,  -270,  -270,  -270,   104,   332,   372,  -270,  -270,
      61,  -270,   349,   379,   173,   170,  -270,  -270,   -49,  -270,
    -270,   -16,  -270,  -270,  -270,  -270,  -270,  -270,  -270,   317,
    -270,    97,   355,  -270,   286,   345,  -270,   386,  -270,  -270,
    -270,   422,  -270,  -270,  -270,  -270,   142,   243,   337,   393,
    -270,   345,  -270,  -270,  -270,     1,  -270,  -270,   155,  -270,
    -270,    98,   370,  -270,  -270,  -270,   404,  -270,   309,   347,
     345,  -270,   311,  -270
};

/* YYPGOTO[NTERM-NUM].  */
static const yytype_int16 yypgoto[] =
{
    -270,  -270,  -270,  -270,  -270,  -270,   356,  -270,   449,  -270,
    -270,  -270,   168,  -270,  -270,  -270,  -270,  -270,  -269,  -270,
    -270,  -270,  -270,   113,    64,  -270,    71,  -270,   118,  -270,
    -101,  -270,   400,  -270,  -270,  -112,  -110,  -270,   397,   334,
    -270,   360,   359,  -270,  -270,  -270,  -270,   238,  -270,  -270,
    -270,  -270,  -270,  -270,  -117,  -116,  -149,  -270,  -270,  -270,
    -143,  -270,  -100,   203
};

/* YYTABLE[YYPACT[STATE-NUM]].  What to do in state STATE-NUM.  If
   positive, shift that token.  If negative, reduce the rule which
   number is the opposite.  If zero, do what YYDEFACT says.
   If YYTABLE_NINF, syntax error.  */
#define YYTABLE_NINF -134
static const yytype_int16 yytable[] =
{
     156,   157,   131,   274,   137,   142,    64,     4,   -19,   275,
      -8,    63,    -8,    -8,    10,    11,   319,    66,   299,   344,
     300,    13,    65,   346,   330,   124,    16,   125,   240,    18,
     241,    20,   132,   133,   134,   174,    67,   306,   321,   278,
      24,    25,    26,    27,    28,    29,    30,    31,    32,    33,
      34,    35,    36,    37,    38,    39,    40,    41,    42,    43,
      44,    45,    46,    47,    48,    69,   143,   177,   178,   179,
     180,   181,   182,   183,   184,   185,   186,   187,   188,   189,
     190,   191,   192,   193,   194,   195,   363,   345,   347,    73,
     272,   196,    68,    -6,   273,   135,   132,   133,   134,   128,
     149,   132,   133,   134,    76,   197,   198,   199,   200,   201,
     202,   203,   204,   205,   206,   207,   208,   209,   210,   211,
     212,   213,   214,   215,   216,   217,   218,   219,   220,   221,
     275,   240,   271,   241,   222,   223,   224,   225,   226,   227,
     228,   229,   230,   231,   232,   233,   234,   235,   236,   237,
     238,   239,   129,   150,   101,   112,   151,   152,   287,   298,
     307,   153,   114,   293,   154,   349,   366,    70,   299,    71,
     300,   290,   291,   133,   134,   267,   268,   145,   337,    72,
     348,   299,   316,   300,   146,   272,   165,   320,   301,   273,
     338,   339,   288,   334,   308,   102,   154,   333,    78,   350,
     367,   301,   340,   303,    93,   304,    94,    95,   325,    79,
     326,   327,    85,   328,   343,    87,   108,     3,   263,   356,
      86,   357,     4,     5,    89,     6,     7,     8,     9,    10,
      11,    12,   364,    91,   365,   362,    13,    14,    15,   305,
     268,    16,    17,    90,    18,    19,    20,    88,    21,    22,
      23,   109,    99,   372,   103,    24,    25,    26,    27,    28,
      29,    30,    31,    32,    33,    34,    35,    36,    37,    38,
      39,    40,    41,    42,    43,    44,    45,    46,    47,    48,
     104,   110,   358,   359,   282,   283,   105,   -22,   106,   107,
     138,   108,     3,   119,   120,   121,   130,     4,     5,   139,
       6,     7,     8,     9,    10,    11,    12,  -133,  -133,  -133,
    -133,    13,    14,    15,   144,    91,    16,    17,   141,    18,
      19,    20,    73,    21,    22,    23,   109,   148,   108,   164,
      24,    25,    26,    27,    28,    29,    30,    31,    32,    33,
      34,    35,    36,    37,    38,    39,    40,    41,    42,    43,
      44,    45,    46,    47,    48,   168,   110,   170,   175,   169,
    -133,   171,   176,  -133,  -133,   260,   270,  -133,  -133,   276,
     277,  -133,   149,   132,   133,   134,   279,   280,   149,   132,
     133,   134,   281,   286,   149,   132,   133,   134,   295,   261,
      91,   262,   296,   297,   302,   313,   249,   250,   251,   252,
     314,   253,   309,  -133,   263,   330,   254,   255,   322,   264,
     256,   331,   323,   265,   257,   258,   259,   335,   266,   336,
     154,   324,   352,   351,   263,   150,   353,   337,   151,   152,
     360,   150,   361,   153,   151,   152,   154,   150,   368,   153,
     151,   152,   154,   369,   370,   153,     2,   373,   154,   371,
      50,     3,   317,   123,   354,    83,     4,     5,    84,     6,
       7,     8,     9,    10,    11,    12,   294,     0,   155,   172,
      13,    14,    15,   147,   310,    16,    17,   163,    18,    19,
      20,   289,    21,    22,    23,     0,     0,     0,     0,    24,
      25,    26,    27,    28,    29,    30,    31,    32,    33,    34,
      35,    36,    37,    38,    39,    40,    41,    42,    43,    44,
      45,    46,    47,    48,     3,     0,     0,     0,     0,     4,
       0,     0,     0,    82,     0,     0,    10,    11,     0,     0,
       0,     0,     0,    13,     0,    15,     0,     0,    16,    17,
       0,    18,     0,    20,     0,     0,     0,     0,     0,     0,
       0,     0,    24,    25,    26,    27,    28,    29,    30,    31,
      32,    33,    34,    35,    36,    37,    38,    39,    40,    41,
      42,    43,    44,    45,    46,    47,    48,    24,    25,    26,
      27,    28,    29,    30,    31,    32,    33,    34,    35,    36,
      37,    38,    39,    40,    41,    42,    43,    44,    45
};

static const yytype_int16 yycheck[] =
{
     117,   117,   103,   152,   104,    39,    39,    10,    39,   152,
      20,    40,    22,    23,    17,    18,   285,    40,    77,    68,
      79,    24,    16,    39,    40,    24,    29,    26,   140,    32,
     140,    34,    40,    41,    42,   135,    40,    39,    97,   155,
      43,    44,    45,    46,    47,    48,    49,    50,    51,    52,
      53,    54,    55,    56,    57,    58,    59,    60,    61,    62,
      63,    64,    65,    66,    67,    39,   100,    70,    71,    72,
      73,    74,    75,    76,    77,    78,    79,    80,    81,    82,
      83,    84,    85,    86,    87,    88,   355,   136,   104,    99,
      92,    94,     3,   103,    96,   103,    40,    41,    42,    40,
      39,    40,    41,    42,   135,   108,   109,   110,   111,   112,
     113,   114,   115,   116,   117,   118,   119,   120,   121,   122,
     123,   124,   125,   126,   127,   128,   129,   130,   131,   132,
     273,   243,    39,   243,   137,   138,   139,   140,   141,   142,
     143,   144,   145,   146,   147,   148,   149,   150,   151,   152,
     153,   154,    93,    92,    92,    91,    95,    96,    68,    68,
      68,   100,    91,   263,   103,    68,    68,    42,    77,    40,
      79,    39,    40,    41,    42,    39,    40,   113,     5,    16,
     329,    77,   283,    79,   113,    92,   122,   287,    97,    96,
      17,    18,   102,   310,   102,   133,   103,   136,    99,   102,
     102,    97,    29,    77,    20,    79,    22,    23,    77,    39,
      79,    77,    68,    79,   315,    40,     4,     5,    92,    77,
       3,    79,    10,    11,    68,    13,    14,    15,    16,    17,
      18,    19,    77,   103,    79,   351,    24,    25,    26,    39,
      40,    29,    30,    97,    32,    33,    34,    99,    36,    37,
      38,    39,    39,   370,    68,    43,    44,    45,    46,    47,
      48,    49,    50,    51,    52,    53,    54,    55,    56,    57,
      58,    59,    60,    61,    62,    63,    64,    65,    66,    67,
     104,    69,    39,    40,   166,   167,    39,   135,    40,    39,
      68,     4,     5,    40,    40,    40,    40,    10,    11,    68,
      13,    14,    15,    16,    17,    18,    19,    39,    40,    41,
      42,    24,    25,    26,   102,   103,    29,    30,    98,    32,
      33,    34,    99,    36,    37,    38,    39,    99,     4,    68,
      43,    44,    45,    46,    47,    48,    49,    50,    51,    52,
      53,    54,    55,    56,    57,    58,    59,    60,    61,    62,
      63,    64,    65,    66,    67,   136,    69,    93,    40,   135,
      92,   134,    39,    95,    96,    39,   107,    99,   100,    39,
      39,   103,    39,    40,    41,    42,    68,    99,    39,    40,
      41,    42,    40,   102,    39,    40,    41,    42,    40,    77,
     103,    79,    39,    39,    93,    68,    71,    72,    73,    74,
      12,    76,   136,   135,    92,    40,    81,    82,    93,    97,
      85,    39,    93,   101,    89,    90,    91,    68,   106,    40,
     103,    93,   136,    68,    92,    92,    40,     5,    95,    96,
      93,    92,    39,   100,    95,    96,   103,    92,    68,   100,
      95,    96,   103,    39,   135,   100,     0,   136,   103,   102,
       1,     5,   284,    97,   341,    55,    10,    11,    61,    13,
      14,    15,    16,    17,    18,    19,   263,    -1,   135,   135,
      24,    25,    26,   113,   135,    29,    30,   118,    32,    33,
      34,   243,    36,    37,    38,    -1,    -1,    -1,    -1,    43,
      44,    45,    46,    47,    48,    49,    50,    51,    52,    53,
      54,    55,    56,    57,    58,    59,    60,    61,    62,    63,
      64,    65,    66,    67,     5,    -1,    -1,    -1,    -1,    10,
      -1,    -1,    -1,    14,    -1,    -1,    17,    18,    -1,    -1,
      -1,    -1,    -1,    24,    -1,    26,    -1,    -1,    29,    30,
      -1,    32,    -1,    34,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    43,    44,    45,    46,    47,    48,    49,    50,
      51,    52,    53,    54,    55,    56,    57,    58,    59,    60,
      61,    62,    63,    64,    65,    66,    67,    43,    44,    45,
      46,    47,    48,    49,    50,    51,    52,    53,    54,    55,
      56,    57,    58,    59,    60,    61,    62,    63,    64
};

/* YYSTOS[STATE-NUM] -- The (internal number of the) accessing
   symbol of state STATE-NUM.  */
static const yytype_uint8 yystos[] =
{
       0,   156,     0,     5,    10,    11,    13,    14,    15,    16,
      17,    18,    19,    24,    25,    26,    29,    30,    32,    33,
      34,    36,    37,    38,    43,    44,    45,    46,    47,    48,
      49,    50,    51,    52,    53,    54,    55,    56,    57,    58,
      59,    60,    61,    62,    63,    64,    65,    66,    67,   157,
     163,   170,   181,   182,   183,   186,   187,   188,   189,   190,
     191,   192,   193,    40,    39,    16,    40,    40,     3,    39,
      42,    40,    16,    99,   158,   159,   135,   166,    99,    39,
     184,   185,    14,   187,   193,    68,     3,    40,    99,    68,
      97,   103,   179,    20,    22,    23,   161,   162,   164,    39,
     167,    92,   133,    68,   104,    39,    40,    39,     4,    39,
      69,   163,   179,   180,   181,   196,   197,   199,   201,    40,
      40,    40,   160,   161,    24,    26,   173,   168,    40,    93,
      40,   185,    40,    41,    42,   103,   194,   217,    68,    68,
     200,    98,    39,   100,   102,   179,   181,   196,    99,    39,
      92,    95,    96,   100,   103,   135,   209,   210,   211,   212,
     214,   215,   217,   197,    68,   179,   174,   175,   136,   135,
      93,   134,   194,   195,   217,    40,    39,    70,    71,    72,
      73,    74,    75,    76,    77,    78,    79,    80,    81,    82,
      83,    84,    85,    86,    87,    88,    94,   108,   109,   110,
     111,   112,   113,   114,   115,   116,   117,   118,   119,   120,
     121,   122,   123,   124,   125,   126,   127,   128,   129,   130,
     131,   132,   137,   138,   139,   140,   141,   142,   143,   144,
     145,   146,   147,   148,   149,   150,   151,   152,   153,   154,
     190,   191,   202,   203,   204,   205,   206,   207,   208,    71,
      72,    73,    74,    76,    81,    82,    85,    89,    90,    91,
      39,    77,    79,    92,    97,   101,   106,    39,    40,   218,
     107,    39,    92,    96,   211,   215,    39,    39,   210,    68,
      99,    40,   183,   183,   165,   169,   102,    68,   102,   202,
      39,    40,   216,   217,   218,    40,    39,    39,    68,    77,
      79,    97,    93,    77,    79,    39,    39,    68,   102,   136,
     135,   209,   210,    68,    12,   176,   185,   167,   171,   173,
     217,    97,    93,    93,    93,    77,    79,    77,    79,   213,
      40,    39,   198,   136,   209,    68,    40,     5,    17,    18,
      29,   177,   178,   185,    68,   136,    39,   104,   211,    68,
     102,    68,   136,    40,   178,   172,    77,    79,    39,    40,
      93,    39,   210,   173,    77,    79,    68,   102,    68,    39,
     135,   102,   209,   136
};

#define yyerrok		(yyerrstatus = 0)
#define yyclearin	(yychar = YYEMPTY)
#define YYEMPTY		(-2)
#define YYEOF		0

#define YYACCEPT	goto yyacceptlab
#define YYABORT		goto yyabortlab
#define YYERROR		goto yyerrorlab


/* Like YYERROR except do call yyerror.  This remains here temporarily
   to ease the transition to the new meaning of YYERROR, for GCC.
   Once GCC version 2 has supplanted version 1, this can go.  */

#define YYFAIL		goto yyerrlab

#define YYRECOVERING()  (!!yyerrstatus)

#define YYBACKUP(Token, Value)					\
do								\
  if (yychar == YYEMPTY && yylen == 1)				\
    {								\
      yychar = (Token);						\
      yylval = (Value);						\
      yytoken = YYTRANSLATE (yychar);				\
      YYPOPSTACK (1);						\
      goto yybackup;						\
    }								\
  else								\
    {								\
      yyerror (YY_("syntax error: cannot back up")); \
      YYERROR;							\
    }								\
while (YYID (0))


#define YYTERROR	1
#define YYERRCODE	256


/* YYLLOC_DEFAULT -- Set CURRENT to span from RHS[1] to RHS[N].
   If N is 0, then set CURRENT to the empty location which ends
   the previous symbol: RHS[0] (always defined).  */

#define YYRHSLOC(Rhs, K) ((Rhs)[K])
#ifndef YYLLOC_DEFAULT
# define YYLLOC_DEFAULT(Current, Rhs, N)				\
    do									\
      if (YYID (N))                                                    \
	{								\
	  (Current).first_line   = YYRHSLOC (Rhs, 1).first_line;	\
	  (Current).first_column = YYRHSLOC (Rhs, 1).first_column;	\
	  (Current).last_line    = YYRHSLOC (Rhs, N).last_line;		\
	  (Current).last_column  = YYRHSLOC (Rhs, N).last_column;	\
	}								\
      else								\
	{								\
	  (Current).first_line   = (Current).last_line   =		\
	    YYRHSLOC (Rhs, 0).last_line;				\
	  (Current).first_column = (Current).last_column =		\
	    YYRHSLOC (Rhs, 0).last_column;				\
	}								\
    while (YYID (0))
#endif


/* YY_LOCATION_PRINT -- Print the location on the stream.
   This macro was not mandated originally: define only if we know
   we won't break user code: when these are the locations we know.  */

#ifndef YY_LOCATION_PRINT
# if YYLTYPE_IS_TRIVIAL
#  define YY_LOCATION_PRINT(File, Loc)			\
     fprintf (File, "%d.%d-%d.%d",			\
	      (Loc).first_line, (Loc).first_column,	\
	      (Loc).last_line,  (Loc).last_column)
# else
#  define YY_LOCATION_PRINT(File, Loc) ((void) 0)
# endif
#endif


/* YYLEX -- calling `yylex' with the right arguments.  */

#ifdef YYLEX_PARAM
# define YYLEX yylex (YYLEX_PARAM)
#else
# define YYLEX yylex ()
#endif

/* Enable debugging if requested.  */
#if YYDEBUG

# ifndef YYFPRINTF
#  include <stdio.h> /* INFRINGES ON USER NAME SPACE */
#  define YYFPRINTF fprintf
# endif

# define YYDPRINTF(Args)			\
do {						\
  if (yydebug)					\
    YYFPRINTF Args;				\
} while (YYID (0))

# define YY_SYMBOL_PRINT(Title, Type, Value, Location)			  \
do {									  \
  if (yydebug)								  \
    {									  \
      YYFPRINTF (stderr, "%s ", Title);					  \
      yy_symbol_print (stderr,						  \
		  Type, Value); \
      YYFPRINTF (stderr, "\n");						  \
    }									  \
} while (YYID (0))


/*--------------------------------.
| Print this symbol on YYOUTPUT.  |
`--------------------------------*/

/*ARGSUSED*/
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yy_symbol_value_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep)
#else
static void
yy_symbol_value_print (yyoutput, yytype, yyvaluep)
    FILE *yyoutput;
    int yytype;
    YYSTYPE const * const yyvaluep;
#endif
{
  if (!yyvaluep)
    return;
# ifdef YYPRINT
  if (yytype < YYNTOKENS)
    YYPRINT (yyoutput, yytoknum[yytype], *yyvaluep);
# else
  YYUSE (yyoutput);
# endif
  switch (yytype)
    {
      default:
	break;
    }
}


/*--------------------------------.
| Print this symbol on YYOUTPUT.  |
`--------------------------------*/

#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yy_symbol_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep)
#else
static void
yy_symbol_print (yyoutput, yytype, yyvaluep)
    FILE *yyoutput;
    int yytype;
    YYSTYPE const * const yyvaluep;
#endif
{
  if (yytype < YYNTOKENS)
    YYFPRINTF (yyoutput, "token %s (", yytname[yytype]);
  else
    YYFPRINTF (yyoutput, "nterm %s (", yytname[yytype]);

  yy_symbol_value_print (yyoutput, yytype, yyvaluep);
  YYFPRINTF (yyoutput, ")");
}

/*------------------------------------------------------------------.
| yy_stack_print -- Print the state stack from its BOTTOM up to its |
| TOP (included).                                                   |
`------------------------------------------------------------------*/

#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yy_stack_print (yytype_int16 *bottom, yytype_int16 *top)
#else
static void
yy_stack_print (bottom, top)
    yytype_int16 *bottom;
    yytype_int16 *top;
#endif
{
  YYFPRINTF (stderr, "Stack now");
  for (; bottom <= top; ++bottom)
    YYFPRINTF (stderr, " %d", *bottom);
  YYFPRINTF (stderr, "\n");
}

# define YY_STACK_PRINT(Bottom, Top)				\
do {								\
  if (yydebug)							\
    yy_stack_print ((Bottom), (Top));				\
} while (YYID (0))


/*------------------------------------------------.
| Report that the YYRULE is going to be reduced.  |
`------------------------------------------------*/

#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yy_reduce_print (YYSTYPE *yyvsp, int yyrule)
#else
static void
yy_reduce_print (yyvsp, yyrule)
    YYSTYPE *yyvsp;
    int yyrule;
#endif
{
  int yynrhs = yyr2[yyrule];
  int yyi;
  unsigned long int yylno = yyrline[yyrule];
  YYFPRINTF (stderr, "Reducing stack by rule %d (line %lu):\n",
	     yyrule - 1, yylno);
  /* The symbols being reduced.  */
  for (yyi = 0; yyi < yynrhs; yyi++)
    {
      fprintf (stderr, "   $%d = ", yyi + 1);
      yy_symbol_print (stderr, yyrhs[yyprhs[yyrule] + yyi],
		       &(yyvsp[(yyi + 1) - (yynrhs)])
		       		       );
      fprintf (stderr, "\n");
    }
}

# define YY_REDUCE_PRINT(Rule)		\
do {					\
  if (yydebug)				\
    yy_reduce_print (yyvsp, Rule); \
} while (YYID (0))

/* Nonzero means print parse trace.  It is left uninitialized so that
   multiple parsers can coexist.  */
int yydebug;
#else /* !YYDEBUG */
# define YYDPRINTF(Args)
# define YY_SYMBOL_PRINT(Title, Type, Value, Location)
# define YY_STACK_PRINT(Bottom, Top)
# define YY_REDUCE_PRINT(Rule)
#endif /* !YYDEBUG */


/* YYINITDEPTH -- initial size of the parser's stacks.  */
#ifndef	YYINITDEPTH
# define YYINITDEPTH 200
#endif

/* YYMAXDEPTH -- maximum size the stacks can grow to (effective only
   if the built-in stack extension method is used).

   Do not make this value too large; the results are undefined if
   YYSTACK_ALLOC_MAXIMUM < YYSTACK_BYTES (YYMAXDEPTH)
   evaluated with infinite-precision integer arithmetic.  */

#ifndef YYMAXDEPTH
# define YYMAXDEPTH 10000
#endif



#if YYERROR_VERBOSE

# ifndef yystrlen
#  if defined __GLIBC__ && defined _STRING_H
#   define yystrlen strlen
#  else
/* Return the length of YYSTR.  */
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static YYSIZE_T
yystrlen (const char *yystr)
#else
static YYSIZE_T
yystrlen (yystr)
    const char *yystr;
#endif
{
  YYSIZE_T yylen;
  for (yylen = 0; yystr[yylen]; yylen++)
    continue;
  return yylen;
}
#  endif
# endif

# ifndef yystpcpy
#  if defined __GLIBC__ && defined _STRING_H && defined _GNU_SOURCE
#   define yystpcpy stpcpy
#  else
/* Copy YYSRC to YYDEST, returning the address of the terminating '\0' in
   YYDEST.  */
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static char *
yystpcpy (char *yydest, const char *yysrc)
#else
static char *
yystpcpy (yydest, yysrc)
    char *yydest;
    const char *yysrc;
#endif
{
  char *yyd = yydest;
  const char *yys = yysrc;

  while ((*yyd++ = *yys++) != '\0')
    continue;

  return yyd - 1;
}
#  endif
# endif

# ifndef yytnamerr
/* Copy to YYRES the contents of YYSTR after stripping away unnecessary
   quotes and backslashes, so that it's suitable for yyerror.  The
   heuristic is that double-quoting is unnecessary unless the string
   contains an apostrophe, a comma, or backslash (other than
   backslash-backslash).  YYSTR is taken from yytname.  If YYRES is
   null, do not copy; instead, return the length of what the result
   would have been.  */
static YYSIZE_T
yytnamerr (char *yyres, const char *yystr)
{
  if (*yystr == '"')
    {
      YYSIZE_T yyn = 0;
      char const *yyp = yystr;

      for (;;)
	switch (*++yyp)
	  {
	  case '\'':
	  case ',':
	    goto do_not_strip_quotes;

	  case '\\':
	    if (*++yyp != '\\')
	      goto do_not_strip_quotes;
	    /* Fall through.  */
	  default:
	    if (yyres)
	      yyres[yyn] = *yyp;
	    yyn++;
	    break;

	  case '"':
	    if (yyres)
	      yyres[yyn] = '\0';
	    return yyn;
	  }
    do_not_strip_quotes: ;
    }

  if (! yyres)
    return yystrlen (yystr);

  return yystpcpy (yyres, yystr) - yyres;
}
# endif

/* Copy into YYRESULT an error message about the unexpected token
   YYCHAR while in state YYSTATE.  Return the number of bytes copied,
   including the terminating null byte.  If YYRESULT is null, do not
   copy anything; just return the number of bytes that would be
   copied.  As a special case, return 0 if an ordinary "syntax error"
   message will do.  Return YYSIZE_MAXIMUM if overflow occurs during
   size calculation.  */
static YYSIZE_T
yysyntax_error (char *yyresult, int yystate, int yychar)
{
  int yyn = yypact[yystate];

  if (! (YYPACT_NINF < yyn && yyn <= YYLAST))
    return 0;
  else
    {
      int yytype = YYTRANSLATE (yychar);
      YYSIZE_T yysize0 = yytnamerr (0, yytname[yytype]);
      YYSIZE_T yysize = yysize0;
      YYSIZE_T yysize1;
      int yysize_overflow = 0;
      enum { YYERROR_VERBOSE_ARGS_MAXIMUM = 5 };
      char const *yyarg[YYERROR_VERBOSE_ARGS_MAXIMUM];
      int yyx;

# if 0
      /* This is so xgettext sees the translatable formats that are
	 constructed on the fly.  */
      YY_("syntax error, unexpected %s");
      YY_("syntax error, unexpected %s, expecting %s");
      YY_("syntax error, unexpected %s, expecting %s or %s");
      YY_("syntax error, unexpected %s, expecting %s or %s or %s");
      YY_("syntax error, unexpected %s, expecting %s or %s or %s or %s");
# endif
      char *yyfmt;
      char const *yyf;
      static char const yyunexpected[] = "syntax error, unexpected %s";
      static char const yyexpecting[] = ", expecting %s";
      static char const yyor[] = " or %s";
      char yyformat[sizeof yyunexpected
		    + sizeof yyexpecting - 1
		    + ((YYERROR_VERBOSE_ARGS_MAXIMUM - 2)
		       * (sizeof yyor - 1))];
      char const *yyprefix = yyexpecting;

      /* Start YYX at -YYN if negative to avoid negative indexes in
	 YYCHECK.  */
      int yyxbegin = yyn < 0 ? -yyn : 0;

      /* Stay within bounds of both yycheck and yytname.  */
      int yychecklim = YYLAST - yyn + 1;
      int yyxend = yychecklim < YYNTOKENS ? yychecklim : YYNTOKENS;
      int yycount = 1;

      yyarg[0] = yytname[yytype];
      yyfmt = yystpcpy (yyformat, yyunexpected);

      for (yyx = yyxbegin; yyx < yyxend; ++yyx)
	if (yycheck[yyx + yyn] == yyx && yyx != YYTERROR)
	  {
	    if (yycount == YYERROR_VERBOSE_ARGS_MAXIMUM)
	      {
		yycount = 1;
		yysize = yysize0;
		yyformat[sizeof yyunexpected - 1] = '\0';
		break;
	      }
	    yyarg[yycount++] = yytname[yyx];
	    yysize1 = yysize + yytnamerr (0, yytname[yyx]);
	    yysize_overflow |= (yysize1 < yysize);
	    yysize = yysize1;
	    yyfmt = yystpcpy (yyfmt, yyprefix);
	    yyprefix = yyor;
	  }

      yyf = YY_(yyformat);
      yysize1 = yysize + yystrlen (yyf);
      yysize_overflow |= (yysize1 < yysize);
      yysize = yysize1;

      if (yysize_overflow)
	return YYSIZE_MAXIMUM;

      if (yyresult)
	{
	  /* Avoid sprintf, as that infringes on the user's name space.
	     Don't have undefined behavior even if the translation
	     produced a string with the wrong number of "%s"s.  */
	  char *yyp = yyresult;
	  int yyi = 0;
	  while ((*yyp = *yyf) != '\0')
	    {
	      if (*yyp == '%' && yyf[1] == 's' && yyi < yycount)
		{
		  yyp += yytnamerr (yyp, yyarg[yyi++]);
		  yyf += 2;
		}
	      else
		{
		  yyp++;
		  yyf++;
		}
	    }
	}
      return yysize;
    }
}
#endif /* YYERROR_VERBOSE */


/*-----------------------------------------------.
| Release the memory associated to this symbol.  |
`-----------------------------------------------*/

/*ARGSUSED*/
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yydestruct (const char *yymsg, int yytype, YYSTYPE *yyvaluep)
#else
static void
yydestruct (yymsg, yytype, yyvaluep)
    const char *yymsg;
    int yytype;
    YYSTYPE *yyvaluep;
#endif
{
  YYUSE (yyvaluep);

  if (!yymsg)
    yymsg = "Deleting";
  YY_SYMBOL_PRINT (yymsg, yytype, yyvaluep, yylocationp);

  switch (yytype)
    {

      default:
	break;
    }
}


/* Prevent warnings from -Wmissing-prototypes.  */

#ifdef YYPARSE_PARAM
#if defined __STDC__ || defined __cplusplus
int yyparse (void *YYPARSE_PARAM);
#else
int yyparse ();
#endif
#else /* ! YYPARSE_PARAM */
#if defined __STDC__ || defined __cplusplus
int yyparse (void);
#else
int yyparse ();
#endif
#endif /* ! YYPARSE_PARAM */



/* The look-ahead symbol.  */
int yychar;

/* The semantic value of the look-ahead symbol.  */
YYSTYPE yylval;

/* Number of syntax errors so far.  */
int yynerrs;



/*----------.
| yyparse.  |
`----------*/

#ifdef YYPARSE_PARAM
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
int
yyparse (void *YYPARSE_PARAM)
#else
int
yyparse (YYPARSE_PARAM)
    void *YYPARSE_PARAM;
#endif
#else /* ! YYPARSE_PARAM */
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
int
yyparse (void)
#else
int
yyparse ()

#endif
#endif
{
  
  int yystate;
  int yyn;
  int yyresult;
  /* Number of tokens to shift before error messages enabled.  */
  int yyerrstatus;
  /* Look-ahead token as an internal (translated) token number.  */
  int yytoken = 0;
#if YYERROR_VERBOSE
  /* Buffer for error messages, and its allocated size.  */
  char yymsgbuf[128];
  char *yymsg = yymsgbuf;
  YYSIZE_T yymsg_alloc = sizeof yymsgbuf;
#endif

  /* Three stacks and their tools:
     `yyss': related to states,
     `yyvs': related to semantic values,
     `yyls': related to locations.

     Refer to the stacks thru separate pointers, to allow yyoverflow
     to reallocate them elsewhere.  */

  /* The state stack.  */
  yytype_int16 yyssa[YYINITDEPTH];
  yytype_int16 *yyss = yyssa;
  yytype_int16 *yyssp;

  /* The semantic value stack.  */
  YYSTYPE yyvsa[YYINITDEPTH];
  YYSTYPE *yyvs = yyvsa;
  YYSTYPE *yyvsp;



#define YYPOPSTACK(N)   (yyvsp -= (N), yyssp -= (N))

  YYSIZE_T yystacksize = YYINITDEPTH;

  /* The variables used to return semantic value and location from the
     action routines.  */
  YYSTYPE yyval;


  /* The number of symbols on the RHS of the reduced rule.
     Keep to zero when no symbol should be popped.  */
  int yylen = 0;

  YYDPRINTF ((stderr, "Starting parse\n"));

  yystate = 0;
  yyerrstatus = 0;
  yynerrs = 0;
  yychar = YYEMPTY;		/* Cause a token to be read.  */

  /* Initialize stack pointers.
     Waste one element of value and location stack
     so that they stay on the same level as the state stack.
     The wasted elements are never initialized.  */

  yyssp = yyss;
  yyvsp = yyvs;

  goto yysetstate;

/*------------------------------------------------------------.
| yynewstate -- Push a new state, which is found in yystate.  |
`------------------------------------------------------------*/
 yynewstate:
  /* In all cases, when you get here, the value and location stacks
     have just been pushed.  So pushing a state here evens the stacks.  */
  yyssp++;

 yysetstate:
  *yyssp = yystate;

  if (yyss + yystacksize - 1 <= yyssp)
    {
      /* Get the current used size of the three stacks, in elements.  */
      YYSIZE_T yysize = yyssp - yyss + 1;

#ifdef yyoverflow
      {
	/* Give user a chance to reallocate the stack.  Use copies of
	   these so that the &'s don't force the real ones into
	   memory.  */
	YYSTYPE *yyvs1 = yyvs;
	yytype_int16 *yyss1 = yyss;


	/* Each stack pointer address is followed by the size of the
	   data in use in that stack, in bytes.  This used to be a
	   conditional around just the two extra args, but that might
	   be undefined if yyoverflow is a macro.  */
	yyoverflow (YY_("memory exhausted"),
		    &yyss1, yysize * sizeof (*yyssp),
		    &yyvs1, yysize * sizeof (*yyvsp),

		    &yystacksize);

	yyss = yyss1;
	yyvs = yyvs1;
      }
#else /* no yyoverflow */
# ifndef YYSTACK_RELOCATE
      goto yyexhaustedlab;
# else
      /* Extend the stack our own way.  */
      if (YYMAXDEPTH <= yystacksize)
	goto yyexhaustedlab;
      yystacksize *= 2;
      if (YYMAXDEPTH < yystacksize)
	yystacksize = YYMAXDEPTH;

      {
	yytype_int16 *yyss1 = yyss;
	union yyalloc *yyptr =
	  (union yyalloc *) YYSTACK_ALLOC (YYSTACK_BYTES (yystacksize));
	if (! yyptr)
	  goto yyexhaustedlab;
	YYSTACK_RELOCATE (yyss);
	YYSTACK_RELOCATE (yyvs);

#  undef YYSTACK_RELOCATE
	if (yyss1 != yyssa)
	  YYSTACK_FREE (yyss1);
      }
# endif
#endif /* no yyoverflow */

      yyssp = yyss + yysize - 1;
      yyvsp = yyvs + yysize - 1;


      YYDPRINTF ((stderr, "Stack size increased to %lu\n",
		  (unsigned long int) yystacksize));

      if (yyss + yystacksize - 1 <= yyssp)
	YYABORT;
    }

  YYDPRINTF ((stderr, "Entering state %d\n", yystate));

  goto yybackup;

/*-----------.
| yybackup.  |
`-----------*/
yybackup:

  /* Do appropriate processing given the current state.  Read a
     look-ahead token if we need one and don't already have one.  */

  /* First try to decide what to do without reference to look-ahead token.  */
  yyn = yypact[yystate];
  if (yyn == YYPACT_NINF)
    goto yydefault;

  /* Not known => get a look-ahead token if don't already have one.  */

  /* YYCHAR is either YYEMPTY or YYEOF or a valid look-ahead symbol.  */
  if (yychar == YYEMPTY)
    {
      YYDPRINTF ((stderr, "Reading a token: "));
      yychar = YYLEX;
    }

  if (yychar <= YYEOF)
    {
      yychar = yytoken = YYEOF;
      YYDPRINTF ((stderr, "Now at end of input.\n"));
    }
  else
    {
      yytoken = YYTRANSLATE (yychar);
      YY_SYMBOL_PRINT ("Next token is", yytoken, &yylval, &yylloc);
    }

  /* If the proper action on seeing token YYTOKEN is to reduce or to
     detect an error, take that action.  */
  yyn += yytoken;
  if (yyn < 0 || YYLAST < yyn || yycheck[yyn] != yytoken)
    goto yydefault;
  yyn = yytable[yyn];
  if (yyn <= 0)
    {
      if (yyn == 0 || yyn == YYTABLE_NINF)
	goto yyerrlab;
      yyn = -yyn;
      goto yyreduce;
    }

  if (yyn == YYFINAL)
    YYACCEPT;

  /* Count tokens shifted since error; after three, turn off error
     status.  */
  if (yyerrstatus)
    yyerrstatus--;

  /* Shift the look-ahead token.  */
  YY_SYMBOL_PRINT ("Shifting", yytoken, &yylval, &yylloc);

  /* Discard the shifted token unless it is eof.  */
  if (yychar != YYEOF)
    yychar = YYEMPTY;

  yystate = yyn;
  *++yyvsp = yylval;

  goto yynewstate;


/*-----------------------------------------------------------.
| yydefault -- do the default action for the current state.  |
`-----------------------------------------------------------*/
yydefault:
  yyn = yydefact[yystate];
  if (yyn == 0)
    goto yyerrlab;
  goto yyreduce;


/*-----------------------------.
| yyreduce -- Do a reduction.  |
`-----------------------------*/
yyreduce:
  /* yyn is the number of a rule to reduce with.  */
  yylen = yyr2[yyn];

  /* If YYLEN is nonzero, implement the default value of the action:
     `$$ = $1'.

     Otherwise, the following line sets YYVAL to garbage.
     This behavior is undocumented and Bison
     users should not rely upon it.  Assigning to YYVAL
     unconditionally makes the parser a bit smaller, and it avoids a
     GCC warning that YYVAL may be used uninitialized.  */
  yyval = yyvsp[1-yylen];


  YY_REDUCE_PRINT (yyn);
  switch (yyn)
    {
        case 6:
#line 213 "../src/cuda-sim/ptx.y"
    { set_symtab((yyvsp[(1) - (1)].ptr_value)); func_header(".skip"); ;}
    break;

  case 7:
#line 213 "../src/cuda-sim/ptx.y"
    { end_function(); ;}
    break;

  case 8:
#line 214 "../src/cuda-sim/ptx.y"
    { set_symtab((yyvsp[(1) - (1)].ptr_value)); ;}
    break;

  case 9:
#line 214 "../src/cuda-sim/ptx.y"
    { func_header(".skip"); ;}
    break;

  case 10:
#line 214 "../src/cuda-sim/ptx.y"
    { end_function(); ;}
    break;

  case 11:
#line 217 "../src/cuda-sim/ptx.y"
    {func_header_info_int(".maxntid", (yyvsp[(2) - (6)].int_value));
										func_header_info_int(",", (yyvsp[(4) - (6)].int_value));
										func_header_info_int(",", (yyvsp[(6) - (6)].int_value)); ;}
    break;

  case 12:
#line 220 "../src/cuda-sim/ptx.y"
    { func_header_info_int(".minnctapersm", (yyvsp[(2) - (2)].int_value)); printf("GPGPU-Sim: Warning: .minnctapersm ignored. \n"); ;}
    break;

  case 13:
#line 221 "../src/cuda-sim/ptx.y"
    { func_header_info_int(".maxnctapersm", (yyvsp[(2) - (2)].int_value)); printf("GPGPU-Sim: Warning: .maxnctapersm ignored. \n"); ;}
    break;

  case 16:
#line 228 "../src/cuda-sim/ptx.y"
    { start_function((yyvsp[(1) - (2)].int_value)); func_header_info("(");;}
    break;

  case 17:
#line 228 "../src/cuda-sim/ptx.y"
    {func_header_info(")");;}
    break;

  case 18:
#line 228 "../src/cuda-sim/ptx.y"
    { (yyval.ptr_value) = reset_symtab(); ;}
    break;

  case 19:
#line 229 "../src/cuda-sim/ptx.y"
    { start_function((yyvsp[(1) - (1)].int_value)); ;}
    break;

  case 20:
#line 229 "../src/cuda-sim/ptx.y"
    { (yyval.ptr_value) = reset_symtab(); ;}
    break;

  case 21:
#line 230 "../src/cuda-sim/ptx.y"
    { start_function((yyvsp[(1) - (1)].int_value)); add_function_name(""); g_func_decl=0; (yyval.ptr_value) = reset_symtab(); ;}
    break;

  case 22:
#line 233 "../src/cuda-sim/ptx.y"
    { add_function_name((yyvsp[(1) - (1)].string_value)); ;}
    break;

  case 23:
#line 233 "../src/cuda-sim/ptx.y"
    {func_header_info("(");;}
    break;

  case 24:
#line 233 "../src/cuda-sim/ptx.y"
    { g_func_decl=0; func_header_info(")"); ;}
    break;

  case 25:
#line 234 "../src/cuda-sim/ptx.y"
    { add_function_name((yyvsp[(1) - (1)].string_value)); g_func_decl=0; ;}
    break;

  case 26:
#line 237 "../src/cuda-sim/ptx.y"
    { (yyval.int_value) = 1; g_func_decl=1; func_header(".entry"); ;}
    break;

  case 27:
#line 238 "../src/cuda-sim/ptx.y"
    { (yyval.int_value) = 0; g_func_decl=1; func_header(".func"); ;}
    break;

  case 28:
#line 239 "../src/cuda-sim/ptx.y"
    { (yyval.int_value) = 0; g_func_decl=1; func_header(".func"); ;}
    break;

  case 29:
#line 240 "../src/cuda-sim/ptx.y"
    { (yyval.int_value) = 2; g_func_decl=1; func_header(".func"); ;}
    break;

  case 31:
#line 244 "../src/cuda-sim/ptx.y"
    { add_directive(); ;}
    break;

  case 32:
#line 245 "../src/cuda-sim/ptx.y"
    {func_header_info(",");;}
    break;

  case 33:
#line 245 "../src/cuda-sim/ptx.y"
    { add_directive(); ;}
    break;

  case 34:
#line 247 "../src/cuda-sim/ptx.y"
    { add_space_spec(param_space_unclassified,0); ;}
    break;

  case 35:
#line 247 "../src/cuda-sim/ptx.y"
    { add_function_arg(); ;}
    break;

  case 36:
#line 248 "../src/cuda-sim/ptx.y"
    { add_space_spec(reg_space,0); ;}
    break;

  case 37:
#line 248 "../src/cuda-sim/ptx.y"
    { add_function_arg(); ;}
    break;

  case 41:
#line 254 "../src/cuda-sim/ptx.y"
    { add_ptr_spec(global_space); ;}
    break;

  case 42:
#line 255 "../src/cuda-sim/ptx.y"
    { add_ptr_spec(local_space); ;}
    break;

  case 43:
#line 256 "../src/cuda-sim/ptx.y"
    { add_ptr_spec(shared_space); ;}
    break;

  case 46:
#line 262 "../src/cuda-sim/ptx.y"
    { add_directive(); ;}
    break;

  case 47:
#line 263 "../src/cuda-sim/ptx.y"
    { add_instruction(); ;}
    break;

  case 48:
#line 264 "../src/cuda-sim/ptx.y"
    { add_directive(); ;}
    break;

  case 49:
#line 265 "../src/cuda-sim/ptx.y"
    { add_instruction(); ;}
    break;

  case 53:
#line 271 "../src/cuda-sim/ptx.y"
    { add_version_info((yyvsp[(2) - (2)].double_value), 0); ;}
    break;

  case 54:
#line 272 "../src/cuda-sim/ptx.y"
    { add_version_info((yyvsp[(2) - (3)].double_value),1); ;}
    break;

  case 55:
#line 273 "../src/cuda-sim/ptx.y"
    {/*Do nothing*/;}
    break;

  case 56:
#line 274 "../src/cuda-sim/ptx.y"
    { target_header2((yyvsp[(2) - (4)].string_value),(yyvsp[(4) - (4)].string_value)); ;}
    break;

  case 57:
#line 275 "../src/cuda-sim/ptx.y"
    { target_header3((yyvsp[(2) - (6)].string_value),(yyvsp[(4) - (6)].string_value),(yyvsp[(6) - (6)].string_value)); ;}
    break;

  case 58:
#line 276 "../src/cuda-sim/ptx.y"
    { target_header((yyvsp[(2) - (2)].string_value)); ;}
    break;

  case 59:
#line 277 "../src/cuda-sim/ptx.y"
    { add_file((yyvsp[(2) - (3)].int_value),(yyvsp[(3) - (3)].string_value)); ;}
    break;

  case 61:
#line 279 "../src/cuda-sim/ptx.y"
    { add_pragma((yyvsp[(2) - (3)].string_value)); ;}
    break;

  case 62:
#line 280 "../src/cuda-sim/ptx.y"
    {/*Do nothing*/;}
    break;

  case 63:
#line 283 "../src/cuda-sim/ptx.y"
    { add_variables(); ;}
    break;

  case 64:
#line 284 "../src/cuda-sim/ptx.y"
    { add_variables(); ;}
    break;

  case 65:
#line 285 "../src/cuda-sim/ptx.y"
    { add_variables(); ;}
    break;

  case 66:
#line 286 "../src/cuda-sim/ptx.y"
    { add_constptr((yyvsp[(2) - (6)].string_value), (yyvsp[(4) - (6)].string_value), (yyvsp[(6) - (6)].int_value)); ;}
    break;

  case 67:
#line 289 "../src/cuda-sim/ptx.y"
    { set_variable_type(); ;}
    break;

  case 70:
#line 294 "../src/cuda-sim/ptx.y"
    { add_identifier((yyvsp[(1) - (1)].string_value),0,NON_ARRAY_IDENTIFIER); func_header_info((yyvsp[(1) - (1)].string_value));;}
    break;

  case 71:
#line 295 "../src/cuda-sim/ptx.y"
    { func_header_info((yyvsp[(1) - (4)].string_value)); func_header_info_int("<", (yyvsp[(3) - (4)].int_value)); func_header_info(">");
		int i,lbase,l;
		char *id = NULL;
		lbase = strlen((yyvsp[(1) - (4)].string_value));
		for( i=0; i < (yyvsp[(3) - (4)].int_value); i++ ) { 
			l = lbase + (int)log10(i+1)+10;
			id = (char*) malloc(l);
			snprintf(id,l,"%s%u",(yyvsp[(1) - (4)].string_value),i);
			add_identifier(id,0,NON_ARRAY_IDENTIFIER); 
		}
		free((yyvsp[(1) - (4)].string_value));
	;}
    break;

  case 72:
#line 307 "../src/cuda-sim/ptx.y"
    { add_identifier((yyvsp[(1) - (3)].string_value),0,ARRAY_IDENTIFIER_NO_DIM); func_header_info((yyvsp[(1) - (3)].string_value)); func_header_info("["); func_header_info("]");;}
    break;

  case 73:
#line 308 "../src/cuda-sim/ptx.y"
    { add_identifier((yyvsp[(1) - (4)].string_value),(yyvsp[(3) - (4)].int_value),ARRAY_IDENTIFIER); func_header_info((yyvsp[(1) - (4)].string_value)); func_header_info_int("[",(yyvsp[(3) - (4)].int_value)); func_header_info("]");;}
    break;

  case 79:
#line 317 "../src/cuda-sim/ptx.y"
    { add_extern_spec(); ;}
    break;

  case 80:
#line 320 "../src/cuda-sim/ptx.y"
    { add_alignment_spec((yyvsp[(2) - (2)].int_value)); ;}
    break;

  case 81:
#line 322 "../src/cuda-sim/ptx.y"
    {  add_space_spec(reg_space,0); ;}
    break;

  case 82:
#line 323 "../src/cuda-sim/ptx.y"
    {  add_space_spec(reg_space,0); ;}
    break;

  case 84:
#line 327 "../src/cuda-sim/ptx.y"
    {  add_space_spec(const_space,(yyvsp[(1) - (1)].int_value)); ;}
    break;

  case 85:
#line 328 "../src/cuda-sim/ptx.y"
    {  add_space_spec(global_space,0); ;}
    break;

  case 86:
#line 329 "../src/cuda-sim/ptx.y"
    {  add_space_spec(local_space,0); ;}
    break;

  case 87:
#line 330 "../src/cuda-sim/ptx.y"
    {  add_space_spec(param_space_unclassified,0); ;}
    break;

  case 88:
#line 331 "../src/cuda-sim/ptx.y"
    {  add_space_spec(shared_space,0); ;}
    break;

  case 89:
#line 332 "../src/cuda-sim/ptx.y"
    {  add_space_spec(surf_space,0); ;}
    break;

  case 90:
#line 333 "../src/cuda-sim/ptx.y"
    {  add_space_spec(tex_space,0); ;}
    break;

  case 93:
#line 340 "../src/cuda-sim/ptx.y"
    {  add_option(V2_TYPE); func_header_info(".v2");;}
    break;

  case 94:
#line 341 "../src/cuda-sim/ptx.y"
    {  add_option(V3_TYPE); func_header_info(".v3");;}
    break;

  case 95:
#line 342 "../src/cuda-sim/ptx.y"
    {  add_option(V4_TYPE); func_header_info(".v4");;}
    break;

  case 96:
#line 345 "../src/cuda-sim/ptx.y"
    { add_scalar_type_spec( S8_TYPE ); ;}
    break;

  case 97:
#line 346 "../src/cuda-sim/ptx.y"
    { add_scalar_type_spec( S16_TYPE ); ;}
    break;

  case 98:
#line 347 "../src/cuda-sim/ptx.y"
    { add_scalar_type_spec( S32_TYPE ); ;}
    break;

  case 99:
#line 348 "../src/cuda-sim/ptx.y"
    { add_scalar_type_spec( S64_TYPE ); ;}
    break;

  case 100:
#line 349 "../src/cuda-sim/ptx.y"
    { add_scalar_type_spec( U8_TYPE ); ;}
    break;

  case 101:
#line 350 "../src/cuda-sim/ptx.y"
    { add_scalar_type_spec( U16_TYPE ); ;}
    break;

  case 102:
#line 351 "../src/cuda-sim/ptx.y"
    { add_scalar_type_spec( U32_TYPE ); ;}
    break;

  case 103:
#line 352 "../src/cuda-sim/ptx.y"
    { add_scalar_type_spec( U64_TYPE ); ;}
    break;

  case 104:
#line 353 "../src/cuda-sim/ptx.y"
    { add_scalar_type_spec( F16_TYPE ); ;}
    break;

  case 105:
#line 354 "../src/cuda-sim/ptx.y"
    { add_scalar_type_spec( F32_TYPE ); ;}
    break;

  case 106:
#line 355 "../src/cuda-sim/ptx.y"
    { add_scalar_type_spec( F64_TYPE ); ;}
    break;

  case 107:
#line 356 "../src/cuda-sim/ptx.y"
    { add_scalar_type_spec( FF64_TYPE ); ;}
    break;

  case 108:
#line 357 "../src/cuda-sim/ptx.y"
    { add_scalar_type_spec( B8_TYPE );  ;}
    break;

  case 109:
#line 358 "../src/cuda-sim/ptx.y"
    { add_scalar_type_spec( B16_TYPE ); ;}
    break;

  case 110:
#line 359 "../src/cuda-sim/ptx.y"
    { add_scalar_type_spec( B32_TYPE ); ;}
    break;

  case 111:
#line 360 "../src/cuda-sim/ptx.y"
    { add_scalar_type_spec( B64_TYPE ); ;}
    break;

  case 112:
#line 361 "../src/cuda-sim/ptx.y"
    { add_scalar_type_spec( BB64_TYPE ); ;}
    break;

  case 113:
#line 362 "../src/cuda-sim/ptx.y"
    { add_scalar_type_spec( BB128_TYPE ); ;}
    break;

  case 114:
#line 363 "../src/cuda-sim/ptx.y"
    { add_scalar_type_spec( PRED_TYPE ); ;}
    break;

  case 115:
#line 364 "../src/cuda-sim/ptx.y"
    { add_scalar_type_spec( TEXREF_TYPE ); ;}
    break;

  case 116:
#line 365 "../src/cuda-sim/ptx.y"
    { add_scalar_type_spec( SAMPLERREF_TYPE ); ;}
    break;

  case 117:
#line 366 "../src/cuda-sim/ptx.y"
    { add_scalar_type_spec( SURFREF_TYPE ); ;}
    break;

  case 118:
#line 369 "../src/cuda-sim/ptx.y"
    { add_array_initializer(); ;}
    break;

  case 119:
#line 370 "../src/cuda-sim/ptx.y"
    { syntax_not_implemented(); ;}
    break;

  case 123:
#line 376 "../src/cuda-sim/ptx.y"
    { add_label((yyvsp[(1) - (2)].string_value)); ;}
    break;

  case 125:
#line 379 "../src/cuda-sim/ptx.y"
    { set_return(); ;}
    break;

  case 131:
#line 386 "../src/cuda-sim/ptx.y"
    { add_opcode((yyvsp[(1) - (1)].int_value)); ;}
    break;

  case 133:
#line 387 "../src/cuda-sim/ptx.y"
    { add_opcode((yyvsp[(1) - (1)].int_value)); ;}
    break;

  case 134:
#line 389 "../src/cuda-sim/ptx.y"
    { add_pred((yyvsp[(2) - (2)].string_value),0, -1); ;}
    break;

  case 135:
#line 390 "../src/cuda-sim/ptx.y"
    { add_pred((yyvsp[(3) - (3)].string_value),1, -1); ;}
    break;

  case 136:
#line 391 "../src/cuda-sim/ptx.y"
    { add_pred((yyvsp[(2) - (3)].string_value),0,1); ;}
    break;

  case 137:
#line 392 "../src/cuda-sim/ptx.y"
    { add_pred((yyvsp[(2) - (3)].string_value),0,2); ;}
    break;

  case 138:
#line 393 "../src/cuda-sim/ptx.y"
    { add_pred((yyvsp[(2) - (3)].string_value),0,3); ;}
    break;

  case 139:
#line 394 "../src/cuda-sim/ptx.y"
    { add_pred((yyvsp[(2) - (3)].string_value),0,5); ;}
    break;

  case 140:
#line 395 "../src/cuda-sim/ptx.y"
    { add_pred((yyvsp[(2) - (3)].string_value),0,6); ;}
    break;

  case 141:
#line 396 "../src/cuda-sim/ptx.y"
    { add_pred((yyvsp[(2) - (3)].string_value),0,10); ;}
    break;

  case 142:
#line 397 "../src/cuda-sim/ptx.y"
    { add_pred((yyvsp[(2) - (3)].string_value),0,12); ;}
    break;

  case 143:
#line 398 "../src/cuda-sim/ptx.y"
    { add_pred((yyvsp[(2) - (3)].string_value),0,13); ;}
    break;

  case 144:
#line 399 "../src/cuda-sim/ptx.y"
    { add_pred((yyvsp[(2) - (3)].string_value),0,17); ;}
    break;

  case 145:
#line 400 "../src/cuda-sim/ptx.y"
    { add_pred((yyvsp[(2) - (3)].string_value),0,19); ;}
    break;

  case 146:
#line 401 "../src/cuda-sim/ptx.y"
    { add_pred((yyvsp[(2) - (3)].string_value),0,28); ;}
    break;

  case 153:
#line 411 "../src/cuda-sim/ptx.y"
    { add_option(UNI_OPTION); ;}
    break;

  case 154:
#line 412 "../src/cuda-sim/ptx.y"
    { add_option(WIDE_OPTION); ;}
    break;

  case 155:
#line 413 "../src/cuda-sim/ptx.y"
    { add_option(ANY_OPTION); ;}
    break;

  case 156:
#line 414 "../src/cuda-sim/ptx.y"
    { add_option(ALL_OPTION); ;}
    break;

  case 157:
#line 415 "../src/cuda-sim/ptx.y"
    { add_option(BALLOT_OPTION); ;}
    break;

  case 158:
#line 416 "../src/cuda-sim/ptx.y"
    { add_option(GLOBAL_OPTION); ;}
    break;

  case 159:
#line 417 "../src/cuda-sim/ptx.y"
    { add_option(CTA_OPTION); ;}
    break;

  case 160:
#line 418 "../src/cuda-sim/ptx.y"
    { add_option(SYS_OPTION); ;}
    break;

  case 161:
#line 419 "../src/cuda-sim/ptx.y"
    { add_option(GEOM_MODIFIER_1D); ;}
    break;

  case 162:
#line 420 "../src/cuda-sim/ptx.y"
    { add_option(GEOM_MODIFIER_2D); ;}
    break;

  case 163:
#line 421 "../src/cuda-sim/ptx.y"
    { add_option(GEOM_MODIFIER_3D); ;}
    break;

  case 164:
#line 422 "../src/cuda-sim/ptx.y"
    { add_option(SAT_OPTION); ;}
    break;

  case 165:
#line 423 "../src/cuda-sim/ptx.y"
    { add_option(FTZ_OPTION); ;}
    break;

  case 166:
#line 424 "../src/cuda-sim/ptx.y"
    { add_option(NEG_OPTION); ;}
    break;

  case 167:
#line 425 "../src/cuda-sim/ptx.y"
    { add_option(APPROX_OPTION); ;}
    break;

  case 168:
#line 426 "../src/cuda-sim/ptx.y"
    { add_option(FULL_OPTION); ;}
    break;

  case 169:
#line 427 "../src/cuda-sim/ptx.y"
    { add_option(EXIT_OPTION); ;}
    break;

  case 170:
#line 428 "../src/cuda-sim/ptx.y"
    { add_option(ABS_OPTION); ;}
    break;

  case 172:
#line 430 "../src/cuda-sim/ptx.y"
    { add_option(TO_OPTION); ;}
    break;

  case 173:
#line 431 "../src/cuda-sim/ptx.y"
    { add_option(HALF_OPTION); ;}
    break;

  case 174:
#line 432 "../src/cuda-sim/ptx.y"
    { add_option(CA_OPTION); ;}
    break;

  case 175:
#line 433 "../src/cuda-sim/ptx.y"
    { add_option(CG_OPTION); ;}
    break;

  case 176:
#line 434 "../src/cuda-sim/ptx.y"
    { add_option(CS_OPTION); ;}
    break;

  case 177:
#line 435 "../src/cuda-sim/ptx.y"
    { add_option(LU_OPTION); ;}
    break;

  case 178:
#line 436 "../src/cuda-sim/ptx.y"
    { add_option(CV_OPTION); ;}
    break;

  case 179:
#line 437 "../src/cuda-sim/ptx.y"
    { add_option(WB_OPTION); ;}
    break;

  case 180:
#line 438 "../src/cuda-sim/ptx.y"
    { add_option(WT_OPTION); ;}
    break;

  case 181:
#line 441 "../src/cuda-sim/ptx.y"
    { add_option(ATOMIC_AND); ;}
    break;

  case 182:
#line 442 "../src/cuda-sim/ptx.y"
    { add_option(ATOMIC_OR); ;}
    break;

  case 183:
#line 443 "../src/cuda-sim/ptx.y"
    { add_option(ATOMIC_XOR); ;}
    break;

  case 184:
#line 444 "../src/cuda-sim/ptx.y"
    { add_option(ATOMIC_CAS); ;}
    break;

  case 185:
#line 445 "../src/cuda-sim/ptx.y"
    { add_option(ATOMIC_EXCH); ;}
    break;

  case 186:
#line 446 "../src/cuda-sim/ptx.y"
    { add_option(ATOMIC_ADD); ;}
    break;

  case 187:
#line 447 "../src/cuda-sim/ptx.y"
    { add_option(ATOMIC_INC); ;}
    break;

  case 188:
#line 448 "../src/cuda-sim/ptx.y"
    { add_option(ATOMIC_DEC); ;}
    break;

  case 189:
#line 449 "../src/cuda-sim/ptx.y"
    { add_option(ATOMIC_MIN); ;}
    break;

  case 190:
#line 450 "../src/cuda-sim/ptx.y"
    { add_option(ATOMIC_MAX); ;}
    break;

  case 193:
#line 456 "../src/cuda-sim/ptx.y"
    { add_option(RN_OPTION); ;}
    break;

  case 194:
#line 457 "../src/cuda-sim/ptx.y"
    { add_option(RZ_OPTION); ;}
    break;

  case 195:
#line 458 "../src/cuda-sim/ptx.y"
    { add_option(RM_OPTION); ;}
    break;

  case 196:
#line 459 "../src/cuda-sim/ptx.y"
    { add_option(RP_OPTION); ;}
    break;

  case 197:
#line 462 "../src/cuda-sim/ptx.y"
    { add_option(RNI_OPTION); ;}
    break;

  case 198:
#line 463 "../src/cuda-sim/ptx.y"
    { add_option(RZI_OPTION); ;}
    break;

  case 199:
#line 464 "../src/cuda-sim/ptx.y"
    { add_option(RMI_OPTION); ;}
    break;

  case 200:
#line 465 "../src/cuda-sim/ptx.y"
    { add_option(RPI_OPTION); ;}
    break;

  case 201:
#line 468 "../src/cuda-sim/ptx.y"
    { add_option(EQ_OPTION); ;}
    break;

  case 202:
#line 469 "../src/cuda-sim/ptx.y"
    { add_option(NE_OPTION); ;}
    break;

  case 203:
#line 470 "../src/cuda-sim/ptx.y"
    { add_option(LT_OPTION); ;}
    break;

  case 204:
#line 471 "../src/cuda-sim/ptx.y"
    { add_option(LE_OPTION); ;}
    break;

  case 205:
#line 472 "../src/cuda-sim/ptx.y"
    { add_option(GT_OPTION); ;}
    break;

  case 206:
#line 473 "../src/cuda-sim/ptx.y"
    { add_option(GE_OPTION); ;}
    break;

  case 207:
#line 474 "../src/cuda-sim/ptx.y"
    { add_option(LO_OPTION); ;}
    break;

  case 208:
#line 475 "../src/cuda-sim/ptx.y"
    { add_option(LS_OPTION); ;}
    break;

  case 209:
#line 476 "../src/cuda-sim/ptx.y"
    { add_option(HI_OPTION); ;}
    break;

  case 210:
#line 477 "../src/cuda-sim/ptx.y"
    { add_option(HS_OPTION); ;}
    break;

  case 211:
#line 478 "../src/cuda-sim/ptx.y"
    { add_option(EQU_OPTION); ;}
    break;

  case 212:
#line 479 "../src/cuda-sim/ptx.y"
    { add_option(NEU_OPTION); ;}
    break;

  case 213:
#line 480 "../src/cuda-sim/ptx.y"
    { add_option(LTU_OPTION); ;}
    break;

  case 214:
#line 481 "../src/cuda-sim/ptx.y"
    { add_option(LEU_OPTION); ;}
    break;

  case 215:
#line 482 "../src/cuda-sim/ptx.y"
    { add_option(GTU_OPTION); ;}
    break;

  case 216:
#line 483 "../src/cuda-sim/ptx.y"
    { add_option(GEU_OPTION); ;}
    break;

  case 217:
#line 484 "../src/cuda-sim/ptx.y"
    { add_option(NUM_OPTION); ;}
    break;

  case 218:
#line 485 "../src/cuda-sim/ptx.y"
    { add_option(NAN_OPTION); ;}
    break;

  case 221:
#line 491 "../src/cuda-sim/ptx.y"
    { add_scalar_operand( (yyvsp[(1) - (1)].string_value) ); ;}
    break;

  case 222:
#line 492 "../src/cuda-sim/ptx.y"
    { add_neg_pred_operand( (yyvsp[(2) - (2)].string_value) ); ;}
    break;

  case 223:
#line 493 "../src/cuda-sim/ptx.y"
    { add_scalar_operand( (yyvsp[(2) - (2)].string_value) ); change_operand_neg(); ;}
    break;

  case 228:
#line 498 "../src/cuda-sim/ptx.y"
    { change_operand_neg(); ;}
    break;

  case 230:
#line 500 "../src/cuda-sim/ptx.y"
    { add_address_operand((yyvsp[(1) - (3)].string_value),(yyvsp[(3) - (3)].int_value)); ;}
    break;

  case 231:
#line 501 "../src/cuda-sim/ptx.y"
    { add_scalar_operand( (yyvsp[(1) - (2)].string_value) ); change_operand_lohi(1);;}
    break;

  case 232:
#line 502 "../src/cuda-sim/ptx.y"
    { add_scalar_operand( (yyvsp[(2) - (3)].string_value) ); change_operand_lohi(1); change_operand_neg();;}
    break;

  case 233:
#line 503 "../src/cuda-sim/ptx.y"
    { add_scalar_operand( (yyvsp[(1) - (2)].string_value) ); change_operand_lohi(2);;}
    break;

  case 234:
#line 504 "../src/cuda-sim/ptx.y"
    { add_scalar_operand( (yyvsp[(2) - (3)].string_value) ); change_operand_lohi(2); change_operand_neg();;}
    break;

  case 235:
#line 505 "../src/cuda-sim/ptx.y"
    { add_2vector_operand((yyvsp[(1) - (3)].string_value),(yyvsp[(3) - (3)].string_value)); change_double_operand_type(-1);;}
    break;

  case 236:
#line 506 "../src/cuda-sim/ptx.y"
    { add_2vector_operand((yyvsp[(1) - (4)].string_value),(yyvsp[(3) - (4)].string_value)); change_double_operand_type(-1); change_operand_lohi(1);;}
    break;

  case 237:
#line 507 "../src/cuda-sim/ptx.y"
    { add_2vector_operand((yyvsp[(1) - (4)].string_value),(yyvsp[(3) - (4)].string_value)); change_double_operand_type(-1); change_operand_lohi(2);;}
    break;

  case 238:
#line 508 "../src/cuda-sim/ptx.y"
    { add_2vector_operand((yyvsp[(1) - (3)].string_value),(yyvsp[(3) - (3)].string_value)); change_double_operand_type(-3);;}
    break;

  case 239:
#line 509 "../src/cuda-sim/ptx.y"
    { add_2vector_operand((yyvsp[(1) - (4)].string_value),(yyvsp[(3) - (4)].string_value)); change_double_operand_type(-3); change_operand_lohi(1);;}
    break;

  case 240:
#line 510 "../src/cuda-sim/ptx.y"
    { add_2vector_operand((yyvsp[(1) - (4)].string_value),(yyvsp[(3) - (4)].string_value)); change_double_operand_type(-3); change_operand_lohi(2);;}
    break;

  case 241:
#line 513 "../src/cuda-sim/ptx.y"
    { add_2vector_operand((yyvsp[(2) - (5)].string_value),(yyvsp[(4) - (5)].string_value)); ;}
    break;

  case 242:
#line 514 "../src/cuda-sim/ptx.y"
    { add_3vector_operand((yyvsp[(2) - (7)].string_value),(yyvsp[(4) - (7)].string_value),(yyvsp[(6) - (7)].string_value)); ;}
    break;

  case 243:
#line 515 "../src/cuda-sim/ptx.y"
    { add_4vector_operand((yyvsp[(2) - (9)].string_value),(yyvsp[(4) - (9)].string_value),(yyvsp[(6) - (9)].string_value),(yyvsp[(8) - (9)].string_value)); ;}
    break;

  case 244:
#line 516 "../src/cuda-sim/ptx.y"
    { add_1vector_operand((yyvsp[(2) - (3)].string_value)); ;}
    break;

  case 245:
#line 519 "../src/cuda-sim/ptx.y"
    { add_scalar_operand((yyvsp[(2) - (3)].string_value)); ;}
    break;

  case 247:
#line 524 "../src/cuda-sim/ptx.y"
    { add_builtin_operand((yyvsp[(1) - (2)].int_value),(yyvsp[(2) - (2)].int_value)); ;}
    break;

  case 248:
#line 525 "../src/cuda-sim/ptx.y"
    { add_builtin_operand((yyvsp[(1) - (1)].int_value),-1); ;}
    break;

  case 249:
#line 528 "../src/cuda-sim/ptx.y"
    { add_memory_operand(); ;}
    break;

  case 250:
#line 529 "../src/cuda-sim/ptx.y"
    { add_memory_operand(); change_memory_addr_space((yyvsp[(1) - (4)].string_value)); ;}
    break;

  case 251:
#line 530 "../src/cuda-sim/ptx.y"
    { change_memory_addr_space((yyvsp[(1) - (4)].string_value)); ;}
    break;

  case 252:
#line 531 "../src/cuda-sim/ptx.y"
    { change_memory_addr_space((yyvsp[(1) - (4)].string_value)); add_memory_operand();;}
    break;

  case 253:
#line 532 "../src/cuda-sim/ptx.y"
    { change_operand_neg(); ;}
    break;

  case 254:
#line 535 "../src/cuda-sim/ptx.y"
    { add_double_operand((yyvsp[(1) - (3)].string_value),(yyvsp[(3) - (3)].string_value)); change_double_operand_type(1); ;}
    break;

  case 255:
#line 536 "../src/cuda-sim/ptx.y"
    { add_double_operand((yyvsp[(1) - (4)].string_value),(yyvsp[(3) - (4)].string_value)); change_double_operand_type(1); change_operand_lohi(1); ;}
    break;

  case 256:
#line 537 "../src/cuda-sim/ptx.y"
    { add_double_operand((yyvsp[(1) - (4)].string_value),(yyvsp[(3) - (4)].string_value)); change_double_operand_type(1); change_operand_lohi(2); ;}
    break;

  case 257:
#line 538 "../src/cuda-sim/ptx.y"
    { add_double_operand((yyvsp[(1) - (4)].string_value),(yyvsp[(4) - (4)].string_value)); change_double_operand_type(2); ;}
    break;

  case 258:
#line 539 "../src/cuda-sim/ptx.y"
    { add_double_operand((yyvsp[(1) - (5)].string_value),(yyvsp[(4) - (5)].string_value)); change_double_operand_type(2); change_operand_lohi(1); ;}
    break;

  case 259:
#line 540 "../src/cuda-sim/ptx.y"
    { add_double_operand((yyvsp[(1) - (5)].string_value),(yyvsp[(4) - (5)].string_value)); change_double_operand_type(2); change_operand_lohi(2); ;}
    break;

  case 260:
#line 541 "../src/cuda-sim/ptx.y"
    { add_address_operand((yyvsp[(1) - (4)].string_value),(yyvsp[(4) - (4)].int_value)); change_double_operand_type(3); ;}
    break;

  case 261:
#line 544 "../src/cuda-sim/ptx.y"
    { add_literal_int((yyvsp[(1) - (1)].int_value)); ;}
    break;

  case 262:
#line 545 "../src/cuda-sim/ptx.y"
    { add_literal_float((yyvsp[(1) - (1)].float_value)); ;}
    break;

  case 263:
#line 546 "../src/cuda-sim/ptx.y"
    { add_literal_double((yyvsp[(1) - (1)].double_value)); ;}
    break;

  case 264:
#line 549 "../src/cuda-sim/ptx.y"
    { add_address_operand((yyvsp[(1) - (1)].string_value),0); ;}
    break;

  case 265:
#line 550 "../src/cuda-sim/ptx.y"
    { add_address_operand((yyvsp[(1) - (2)].string_value),0); change_operand_lohi(1);;}
    break;

  case 266:
#line 551 "../src/cuda-sim/ptx.y"
    { add_address_operand((yyvsp[(1) - (2)].string_value),0); change_operand_lohi(2); ;}
    break;

  case 267:
#line 552 "../src/cuda-sim/ptx.y"
    { add_address_operand((yyvsp[(1) - (3)].string_value),(yyvsp[(3) - (3)].int_value)); ;}
    break;

  case 268:
#line 553 "../src/cuda-sim/ptx.y"
    { add_address_operand2((yyvsp[(1) - (1)].int_value)); ;}
    break;


/* Line 1267 of yacc.c.  */
#line 3204 "ptx.tab.c"
      default: break;
    }
  YY_SYMBOL_PRINT ("-> $$ =", yyr1[yyn], &yyval, &yyloc);

  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);

  *++yyvsp = yyval;


  /* Now `shift' the result of the reduction.  Determine what state
     that goes to, based on the state we popped back to and the rule
     number reduced by.  */

  yyn = yyr1[yyn];

  yystate = yypgoto[yyn - YYNTOKENS] + *yyssp;
  if (0 <= yystate && yystate <= YYLAST && yycheck[yystate] == *yyssp)
    yystate = yytable[yystate];
  else
    yystate = yydefgoto[yyn - YYNTOKENS];

  goto yynewstate;


/*------------------------------------.
| yyerrlab -- here on detecting error |
`------------------------------------*/
yyerrlab:
  /* If not already recovering from an error, report this error.  */
  if (!yyerrstatus)
    {
      ++yynerrs;
#if ! YYERROR_VERBOSE
      yyerror (YY_("syntax error"));
#else
      {
	YYSIZE_T yysize = yysyntax_error (0, yystate, yychar);
	if (yymsg_alloc < yysize && yymsg_alloc < YYSTACK_ALLOC_MAXIMUM)
	  {
	    YYSIZE_T yyalloc = 2 * yysize;
	    if (! (yysize <= yyalloc && yyalloc <= YYSTACK_ALLOC_MAXIMUM))
	      yyalloc = YYSTACK_ALLOC_MAXIMUM;
	    if (yymsg != yymsgbuf)
	      YYSTACK_FREE (yymsg);
	    yymsg = (char *) YYSTACK_ALLOC (yyalloc);
	    if (yymsg)
	      yymsg_alloc = yyalloc;
	    else
	      {
		yymsg = yymsgbuf;
		yymsg_alloc = sizeof yymsgbuf;
	      }
	  }

	if (0 < yysize && yysize <= yymsg_alloc)
	  {
	    (void) yysyntax_error (yymsg, yystate, yychar);
	    yyerror (yymsg);
	  }
	else
	  {
	    yyerror (YY_("syntax error"));
	    if (yysize != 0)
	      goto yyexhaustedlab;
	  }
      }
#endif
    }



  if (yyerrstatus == 3)
    {
      /* If just tried and failed to reuse look-ahead token after an
	 error, discard it.  */

      if (yychar <= YYEOF)
	{
	  /* Return failure if at end of input.  */
	  if (yychar == YYEOF)
	    YYABORT;
	}
      else
	{
	  yydestruct ("Error: discarding",
		      yytoken, &yylval);
	  yychar = YYEMPTY;
	}
    }

  /* Else will try to reuse look-ahead token after shifting the error
     token.  */
  goto yyerrlab1;


/*---------------------------------------------------.
| yyerrorlab -- error raised explicitly by YYERROR.  |
`---------------------------------------------------*/
yyerrorlab:

  /* Pacify compilers like GCC when the user code never invokes
     YYERROR and the label yyerrorlab therefore never appears in user
     code.  */
  if (/*CONSTCOND*/ 0)
     goto yyerrorlab;

  /* Do not reclaim the symbols of the rule which action triggered
     this YYERROR.  */
  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);
  yystate = *yyssp;
  goto yyerrlab1;


/*-------------------------------------------------------------.
| yyerrlab1 -- common code for both syntax error and YYERROR.  |
`-------------------------------------------------------------*/
yyerrlab1:
  yyerrstatus = 3;	/* Each real token shifted decrements this.  */

  for (;;)
    {
      yyn = yypact[yystate];
      if (yyn != YYPACT_NINF)
	{
	  yyn += YYTERROR;
	  if (0 <= yyn && yyn <= YYLAST && yycheck[yyn] == YYTERROR)
	    {
	      yyn = yytable[yyn];
	      if (0 < yyn)
		break;
	    }
	}

      /* Pop the current state because it cannot handle the error token.  */
      if (yyssp == yyss)
	YYABORT;


      yydestruct ("Error: popping",
		  yystos[yystate], yyvsp);
      YYPOPSTACK (1);
      yystate = *yyssp;
      YY_STACK_PRINT (yyss, yyssp);
    }

  if (yyn == YYFINAL)
    YYACCEPT;

  *++yyvsp = yylval;


  /* Shift the error token.  */
  YY_SYMBOL_PRINT ("Shifting", yystos[yyn], yyvsp, yylsp);

  yystate = yyn;
  goto yynewstate;


/*-------------------------------------.
| yyacceptlab -- YYACCEPT comes here.  |
`-------------------------------------*/
yyacceptlab:
  yyresult = 0;
  goto yyreturn;

/*-----------------------------------.
| yyabortlab -- YYABORT comes here.  |
`-----------------------------------*/
yyabortlab:
  yyresult = 1;
  goto yyreturn;

#ifndef yyoverflow
/*-------------------------------------------------.
| yyexhaustedlab -- memory exhaustion comes here.  |
`-------------------------------------------------*/
yyexhaustedlab:
  yyerror (YY_("memory exhausted"));
  yyresult = 2;
  /* Fall through.  */
#endif

yyreturn:
  if (yychar != YYEOF && yychar != YYEMPTY)
     yydestruct ("Cleanup: discarding lookahead",
		 yytoken, &yylval);
  /* Do not reclaim the symbols of the rule which action triggered
     this YYABORT or YYACCEPT.  */
  YYPOPSTACK (yylen);
  YY_STACK_PRINT (yyss, yyssp);
  while (yyssp != yyss)
    {
      yydestruct ("Cleanup: popping",
		  yystos[*yyssp], yyvsp);
      YYPOPSTACK (1);
    }
#ifndef yyoverflow
  if (yyss != yyssa)
    YYSTACK_FREE (yyss);
#endif
#if YYERROR_VERBOSE
  if (yymsg != yymsgbuf)
    YYSTACK_FREE (yymsg);
#endif
  /* Make sure YYID is used.  */
  return YYID (yyresult);
}


#line 556 "../src/cuda-sim/ptx.y"


extern int ptx_lineno;
extern const char *g_filename;

void syntax_not_implemented()
{
	printf("Parse error (%s:%u): this syntax is not (yet) implemented:\n",g_filename,ptx_lineno);
	ptx_error(NULL);
	abort();
}

