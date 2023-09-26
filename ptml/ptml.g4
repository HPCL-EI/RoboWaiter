grammar ptml;

tree    : internal_node (Names|tree)+
        ;
internal_node : 'sequence' | 'selector' | 'parallel' | 'decorator';
Names : [a-zA-Z_][a-zA-Z_0-9]* ;