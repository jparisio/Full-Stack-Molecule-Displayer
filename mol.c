#include "mol.h"


void atomset( atom *atom, char element[3], double *x, double *y, double *z ){

    atom->x = *x;
    atom->y = *y;
    atom->z = *z;

    strcpy(atom->element,element);

}

void atomget( atom *atom, char element[3], double *x, double *y, double *z ){

    *x = atom->x;
    *y = atom->y;
    *z = atom->z;

    strcpy(element,atom->element);  

}


void bondset( bond *bond, unsigned short *a1, unsigned short *a2, atom
**atoms, unsigned char *epairs ){
    //are we still copying address of atom structures so we dont dereference the atom structs?
    bond->a1 = *a1;
    bond->a2 = *a2;
    bond->atoms = *atoms;
    bond->epairs = *epairs;
    compute_coords(bond);
}

void bondget( bond *bond, unsigned short *a1, unsigned short *a2, atom
**atoms, unsigned char *epairs ){
    *a1 = bond->a1;
    *a2 = bond->a2;
    *atoms = bond->atoms;
    *epairs = bond->epairs;
}


void compute_coords( bond *bond ){
    //x coords
    bond->x1 = bond->atoms[bond->a1].x;
    bond->x2 = bond->atoms[bond->a2].x;
    //y coords
    bond->y1 = bond->atoms[bond->a1].y;
    bond->y2 = bond->atoms[bond->a2].y;
    //z coord
    bond->z = (bond->atoms[bond->a1].z + bond->atoms[bond->a2].z)/2;
    //len
    bond->len = sqrt(pow(bond->x2 - bond->x1,2) + pow(bond->y2 - bond->y1,2));
    //dx
    bond->dx = (bond->x2 - bond->x1) / bond->len;
    //dy
    bond->dy = (bond->y2 - bond->y1) / bond->len;
    
}


molecule *molmalloc( unsigned short atom_max, unsigned short bond_max ){
    molecule *newMol = malloc(sizeof(molecule));
    //atoms
    newMol->atom_max = atom_max;
    newMol->atom_no = 0;
    newMol->atom_ptrs = malloc(sizeof(struct atom)*atom_max); //ask what the size should be
    newMol->atoms = malloc(sizeof(struct atom)*atom_max);
    //bonds
    newMol->bond_max = bond_max;
    newMol->bond_no = 0;
    newMol->bonds = malloc(sizeof(struct bond)*bond_max);
    newMol->bond_ptrs = malloc(sizeof(struct bond)*bond_max);

    return newMol;
}


molecule *molcopy( molecule *src ){

    molecule *newMol = molmalloc(src->atom_max, src->bond_max);

    // append all atoms and bonds
    for(int i = 0; i < src->atom_no; i++){
        molappend_atom(newMol,&src->atoms[i]);
    }

    for(int i = 0; i < src->bond_no; i++){
        molappend_bond(newMol,&src->bonds[i]);
    }

    return newMol;

}


void molfree( molecule *ptr ){

    free(ptr->atom_ptrs);
    free(ptr->atoms);
    free(ptr->bond_ptrs);
    free(ptr->bonds);
    free(ptr);

}


void molappend_atom( molecule *molecule, atom *atom ){

      //check if the max atoms is set to 0 in which case we set to 1
    if(molecule->atom_max == 0){
        molecule->atom_max = 1;
        molecule->atoms = realloc(molecule->atoms,sizeof(struct atom)*1);
        molecule->atom_ptrs = realloc(molecule->atom_ptrs,sizeof(struct atom)*1);
    }
   
    //checking if max atom storage is equal to the number of atoms in which case we double
    if(molecule->atom_no >= molecule->atom_max){
            molecule->atom_max =  molecule->atom_max * 2;
            molecule->atoms = realloc(molecule->atoms,sizeof(struct atom)*molecule->atom_max);
            molecule->atom_ptrs = realloc(molecule->atom_ptrs,sizeof(struct atom)*molecule->atom_max);
            //set pointers to new atoms after realloc 
            for(int i = 0; i < molecule->atom_no; i++){
                molecule->atom_ptrs[i] = &molecule->atoms[i];
            }
        }
    
    //append atom to list 
    //set the current atom no in the molecule to the atom
    molecule->atoms[molecule->atom_no] = *atom;
    molecule->atom_ptrs[molecule->atom_no] = &molecule->atoms[molecule->atom_no];
    //increment
    molecule->atom_no += 1;

    }



void molappend_bond( molecule *molecule, bond *bond ){
//check if the max atoms is set to 0 in which case we set to 1
    if(molecule->bond_max == 0){
        molecule->bond_max = 1;
        molecule->bonds = realloc(molecule->bonds,sizeof(struct bond)*1);
        molecule->bond_ptrs = realloc(molecule->bond_ptrs,sizeof(struct bond)*1);
    }
    //checking if max bond storage is equal to the number of bonds in which case we double
    if(molecule->bond_no >= molecule->bond_max){
            molecule->bond_max =  molecule->bond_max * 2;
            molecule-> bonds = realloc(molecule->bonds,sizeof(struct bond)*molecule->bond_max);
            molecule->bond_ptrs = realloc(molecule->bond_ptrs,sizeof(struct bond)*molecule->bond_max);
             //set pointers to new atoms after realloc 
            for(int i = 0; i < molecule->bond_no; i++){
                molecule->bond_ptrs[i] = &molecule->bonds[i];
            }
        }

    //append bond to list 
    //set the current bond no in the molecule to the bond
    molecule->bonds[molecule->bond_no] = *bond;
    molecule->bond_ptrs[molecule->bond_no] = &molecule->bonds[molecule->bond_no];
    //increment
    molecule->bond_no += 1;
}


int bond_comp(const void *a, const void *b){
   if (*(double *)a < *(double *)b) return -1;
   if (*(double *)a > *(double *)b) return 1;
   return 0;
}

void molsort( molecule *molecule ){
    //sort for atoms
    double arr[molecule->atom_no];
    for(int i = 0; i < molecule->atom_no; i++){
        arr[i] = molecule->atoms[i].z;
    }

    qsort(arr, molecule->atom_no,sizeof(double),bond_comp);

    //print (remove this later this is for deugging)
    // for(int i = 0; i < molecule->atom_no; i++){
    //     printf("%f\n",arr[i]);
    // }
    //reassign pointers to the correct values
    for(int i = 0; i < molecule->atom_no; i++){
        for(int j = 0; j < molecule->atom_no; j++){
            if(arr[i] == molecule->atoms[j].z){
                molecule->atom_ptrs[i] = &molecule->atoms[j];
            }
        }
    }

    // sort for bonds
    double arr2[molecule->bond_no];
    for(int i = 0; i < molecule->bond_no; i++){
        arr2[i] = molecule->bonds[i].z;
    }

    qsort(arr2, molecule->bond_no,sizeof(double),bond_comp);

    //print (remove this later this is for deugging)
    // for(int i = 0; i < molecule->bond_no; i++){
    //     printf("%f\n",arr2[i]);
    // }
    //reassign pointers to the correct values
    for(int i = 0; i < molecule->bond_no; i++){
        for(int j = 0; j < molecule->bond_no; j++){
            if(arr2[i] == molecule->bonds[j].z){
                molecule->bond_ptrs[i] = &molecule->bonds[j];
            }
        }
    }
} 


void xrotation( xform_matrix xform_matrix, unsigned short deg ){
double rad = deg * (M_PI / 180.0); 
//calc for each rotation
xform_matrix[0][0] = 1;
xform_matrix[0][1] = 0;
xform_matrix[0][2] = 0;
xform_matrix[1][0] = 0;
xform_matrix[1][1] = cos(rad);
xform_matrix[1][2] = (sin(rad)) * -1;
xform_matrix[2][0] = 0;
xform_matrix[2][1] = sin(rad);
xform_matrix[2][2] = cos(rad);
}

void yrotation( xform_matrix xform_matrix, unsigned short deg ){
double rad = deg * (M_PI / 180.0); 
//calc for each rotation 
xform_matrix[0][0] = cos(rad);
xform_matrix[0][1] = 0;
xform_matrix[0][2] = sin(rad);
xform_matrix[1][0] = 0;
xform_matrix[1][1] = 1;
xform_matrix[1][2] = 0;
xform_matrix[2][0] = (sin(rad)) * -1;
xform_matrix[2][1] = 0;
xform_matrix[2][2] = cos(rad);
}

void zrotation( xform_matrix xform_matrix, unsigned short deg ){
double rad = deg * (M_PI / 180.0); 
//calc for each rotation
xform_matrix[0][0] = cos(rad);
xform_matrix[0][1] = (sin(rad)) * -1;
xform_matrix[0][2] = 0;
xform_matrix[1][0] = sin(rad);
xform_matrix[1][1] = cos(rad);
xform_matrix[1][2] = 0;
xform_matrix[2][0] = 0;
xform_matrix[2][1] = 0;
xform_matrix[2][2] = 1;
}

void mol_xform( molecule *molecule, xform_matrix matrix ){

    for(int i = 0; i < molecule->atom_no; i++){
        double tempx, tempy, tempz;
        tempx = (matrix[0][0] * molecule->atoms[i].x) + (matrix[0][1] * molecule->atoms[i].y) + (matrix[0][2] * molecule->atoms[i].z);
        tempy = (matrix[1][0] * molecule->atoms[i].x) + (matrix[1][1] * molecule->atoms[i].y) + (matrix[1][2] * molecule->atoms[i].z);
        tempz = (matrix[2][0] * molecule->atoms[i].x) + (matrix[2][1] * molecule->atoms[i].y) + (matrix[2][2] * molecule->atoms[i].z);
        //assign the temps to the right spots
        molecule->atoms[i].x = tempx;
        molecule->atoms[i].y = tempy;
        molecule->atoms[i].z = tempz;
    }

    for(int i = 0; i < molecule->bond_no; i++){
        compute_coords(&molecule->bonds[i]);
    }

}








