grammar ptml;

tree    		: internal_node ':' (action_sign|tree)+ EOF;
internal_node   : 'sequence' | 'selector' | 'parallel' Integer | 'decorator' ;
action_sign     : 'act' Names '(' action_parm? ')';
action_parm     : (var_decls|Integer|Float|boolean) (',' (var_decls|Integer|Float|boolean))* ;
var_decls		: var_type Names ;
var_type		: 'int' | 'float' | 'bool' | 'string' ;
boolean         : 'True' | 'False' ;

Names 			: [a-zA-Z_][a-zA-Z_0-9]* ;
Integer         : '-'?[1-9][0-9]* | '0' ;
Float           : [0-9]+'.'[0-9]* | '.'[0-9]+ ;



// comments
LINE_COMMENT    : '//' .*? '\r'?'\n' -> skip ;
// useless
WS				: [ \t\u000C\r\n]+ -> skip ;
