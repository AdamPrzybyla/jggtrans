/* $Id: forms.c,v 1.1 2003/04/11 13:18:20 jajcus Exp $ */

/*
 *  (C) Copyright 2002 Jacek Konieczny <jajcus@pld.org.pl>
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License Version 2 as
 *  published by the Free Software Foundation.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
 */

#include "ggtrans.h"

/*
 * adds a field to a jabber:x:data form
 * returns the field added
 */
xmlnode form_add_field(xmlnode form,const char *type,const char *var,
				const char *label,const char *val,int required){
xmlnode field,value;

	field=xmlnode_insert_tag(form,"field");
	xmlnode_put_attrib(field,"type",type);
	xmlnode_put_attrib(field,"var",var);
	if (required) xmlnode_insert_tag(field,"required");
	xmlnode_put_attrib(field,"label",label);
	if (val) {
		value=xmlnode_insert_tag(field,"value");
		xmlnode_insert_cdata(value,val,-1); 
	}	
	return field;
}

/*
 * adds an option to list field of jabber:x:data form
 * returns the node added
 */
xmlnode form_add_option(xmlnode field,const char *label,const char *val){
xmlnode option,value;

	option=xmlnode_insert_tag(field,"option");
	xmlnode_put_attrib(option,"label",label);
	value=xmlnode_insert_tag(option,"value");
	xmlnode_insert_cdata(value,val,-1); 
	return option;
}


/*
 * adds "fixed" field to a jabber:x:data form
 * returns the field added
 */
xmlnode form_add_fixed(xmlnode form,const char *val){
xmlnode field,value;

	field=xmlnode_insert_tag(form,"field");
	xmlnode_put_attrib(field,"type","fixed");
	value=xmlnode_insert_tag(field,"value");
	xmlnode_insert_cdata(value,val,-1); 
	return field;
}


