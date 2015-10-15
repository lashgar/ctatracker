/* A Bison parser, made by GNU Bison 2.3.  */

/* Skeleton interface for Bison's Yacc-like parsers in C

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
/* Line 1529 of yacc.c.  */
#line 365 "ptx.tab.h"
	YYSTYPE;
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
# define YYSTYPE_IS_TRIVIAL 1
#endif

extern YYSTYPE ptx_lval;

