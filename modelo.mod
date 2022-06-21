set a;
set v;


param referencia_aluno{a};
param referencia_vaga{v};
param peso {a};
param pontos {a};
 
# v - valor do item


param vagas {v} >= 0;
var x{a,v} binary;
 
var lista {i in a, j in v} = if (x[i,j] <= 0) then pontos[i] else x[i,j]-1,;
var destaque {i in a, j in v} = if (x[i,j] >= 1) then 1000 else 0;

maximize Z: sum {i in a, j in v} pontos[i]*x[i,j];

subject to r1 {j in v}:sum {i in a} x[i,j] <= vagas[j]; 
subject to r2 {i in a}:sum {j in v} x[i,j] <= 1; 
subject to r3 {j in v, i in a}:x[i,j]*referencia_aluno[i] = x[i,j]*referencia_vaga[j];









