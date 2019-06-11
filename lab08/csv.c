/*
 * csv.c - Implementation for a csv library
 *
 * Modified from code in Kernighan & Pike, _The Practice of Programming_
 *   Copyright (C) 1999 Lucent Technologies 
 *   Excerpted from 'The Practice of Programming' 
 *   by Brian W. Kernighan and Rob Pike 
 *
 * Kurt Schmidt
 * 3/2018
 *
 * gcc 5.4.0 20160609 on
 * Linux 4.13.0-32-generic
 *
 * EDITOR:  tabstop=2 cols=120
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "csv.h"


static char fieldsep[] = "," ; /* field separator chars */

	/***** Prototypes for local helper functions ******/
static char *advquoted( char* ) ;
static int split( csv_t* ) ;


csv_t* csv_init( FILE *f )
{
	csv_t *rv = (csv_t*) malloc( sizeof( csv_t )) ;
	rv->fin = f ;
	reset( rv ) ;

	return( rv ) ;
}


void kill( csv_t* s )
{
	reset( s ) ;
	free( s ) ;
}

/* TODO
 *  Copy all the functions (but for main) from csvgetline2 here.  Not the prototypes.  You already have them in
 *  csv.h.  Functions that access global CSV data need to be modified, take a pointer to a CSV struct as the first
 *  argument, and any references need to be modified
 */
char* csvgetline( csv_t* c ) {
 	int i, j ;
        char *newl, *news ;

        if( line==NULL ) {                      /* allocate on first call */
                c->maxline = c->maxfield = 1 ;
                c->line = (char*) malloc( c->maxline ) ;
                c->sline = (char*) malloc( c->maxline ) ;
                c->field = (char**) malloc( c->maxfield*sizeof( c->field[0] )) ;
                if( c->line==NULL || c->sline==NULL || c->field==NULL) {
                        reset() ;
                        return NULL ;           /* out of memory */
                }
        }

        for( i=0; (j=getc( fin ))!=EOF && ! endofline(fin,j); i++ ) {
                if( i>=maxline-1 ) {      /* grow line */
                        maxline *= 2;               /* double current size */
                        newl = (char*) realloc( line, maxline ) ;
                        if( newl==NULL ) {
                                reset() ;
                                return NULL ;
                        }
                        line = newl ;
                        news = (char*) realloc( sline, maxline ) ;
                        if( news==NULL ) {
                                reset() ;
                                return NULL ;
                        }
                        sline = news ;
                }
                line[i] = j ;
        }  /* for i */

        line[i] = '\0' ;
        if( split()==NOMEM ) {
                reset() ;
                return NULL;                    /* out of memory */
        }
        return (c==EOF && i==0) ? NULL : line ;
}

/* csvfield:  return pointer to n-th field */
char* csvfield( csv_t* c, int n )
{
	if( n<0 || n>=c->nfield )
		return NULL ;
	return c->field[n] ;
}

/* csvnfield:  return number of fields */
int csvnfield( csv_t* c )
{
	return c->nfield ;
}
