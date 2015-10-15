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
     H_SEPARATOR = 258,
     H_ARCH = 259,
     H_CODEVERSION = 260,
     H_PRODUCER = 261,
     H_HOST = 262,
     H_COMPILESIZE = 263,
     H_IDENTIFIER = 264,
     CODEVERSION = 265,
     STRING = 266,
     FILENAME = 267,
     DECIMAL = 268,
     PTXHEADER = 269,
     ELFHEADER = 270,
     PTXLINE = 271,
     ELFLINE = 272,
     SASSLINE = 273,
     IDENTIFIER = 274,
     NEWLINE = 275
   };
#endif
/* Tokens.  */
#define H_SEPARATOR 258
#define H_ARCH 259
#define H_CODEVERSION 260
#define H_PRODUCER 261
#define H_HOST 262
#define H_COMPILESIZE 263
#define H_IDENTIFIER 264
#define CODEVERSION 265
#define STRING 266
#define FILENAME 267
#define DECIMAL 268
#define PTXHEADER 269
#define ELFHEADER 270
#define PTXLINE 271
#define ELFLINE 272
#define SASSLINE 273
#define IDENTIFIER 274
#define NEWLINE 275




#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef union YYSTYPE
#line 47 "cuobjdump.y"
{
	char* string_value;
}
/* Line 1529 of yacc.c.  */
#line 93 "cuobjdump_parser.h"
	YYSTYPE;
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
# define YYSTYPE_IS_TRIVIAL 1
#endif

extern YYSTYPE cuobjdump_lval;

