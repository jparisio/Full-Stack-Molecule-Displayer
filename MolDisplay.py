import molecule;

radius = { 'H': 25,
           'C': 40,
           'O': 40,
           'N': 40,
         };
element_name = { 'H': 'grey',
                 'C': 'black',
                 'O': 'red',
                 'N': 'blue',
               };
header = """<svg version="1.1" width="1000" height="1000" xmlns="http://www.w3.org/2000/svg">""";
footer = """</svg>""";

offsetx = 500;
offsety = 500;


class Atom:
  def __init__(self, atom):
    self.atom = atom;
    self.z = atom.z;

  def __str__(self):
    return f"{self.atom.element}: {self.atom.x}, {self.atom.y}, {self.atom.z}" 

  def svg(self):
    x = self.atom.x * 100 + offsetx;
    y = self.atom.y * 100 + offsety;
    r = radius[self.atom.element];
    fill = element_name[self.atom.element];
    return ' <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' % (x, y, r, fill);

class Bond:
  def __init__(self, bond):
    self.bond = bond;
    self.z = bond.z;

  def __str__(self):
    return f"""atom1: {self.bond.a1}, atom2: {self.bond.a2}, x1: {self.bond.x1},x2:
            {self.bond.x2}, y1: {self.bond.y1}, y2: {self.bond.y2},z: {self.bond.z}, 
            dx: {self.bond.dx}, dy: {self.bond.dy}, len: {self.bond.len}"""
    
  def svg(self):
    c1x = (self.bond.x1 * 100 + offsetx) + self.bond.dy * 10;
    c1y = (self.bond.y1 * 100 + offsety) - self.bond.dx * 10;
    c2x = (self.bond.x1 * 100 + offsetx) - self.bond.dy * 10;
    c2y = (self.bond.y1 * 100 + offsety ) + self.bond.dx * 10;
    c3x = (self.bond.x2 * 100 + offsetx) - self.bond.dy * 10;
    c3y = (self.bond.y2 * 100 + offsety) + self.bond.dx * 10
    c4x = (self.bond.x2 * 100 + offsetx) + self.bond.dy * 10;
    c4y = (self.bond.y2 * 100 + offsety) - self.bond.dx * 10
    
    return ' <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' % (c1x, c1y, c2x, c2y, c3x, c3y, c4x, c4y);



class Molecule(molecule.molecule):
  def __init__(self):
    super().__init__()

  def __str__(self):
    string = "";
    for i in range(self.atom_no):
      atom = self.get_atom(i);
      string += f"ATOM IS: {atom.element}: {atom.x}, {atom.y}, {atom.z}" 

    for i in range(self.bond_no):
      bond = self.get_bond(i)
      string += f"""BOND IS: atom1: {bond.atoms[bond.a1]}, atom2: {bond.atoms[bond.a2]}, 
      x1: {bond.x1},x2: {bond.x2}, y1: {bond.y1}, y2: {bond.y2},
      z: {bond.z}, dx: {bond.dx}, dy: {bond.dy}, len: {bond.len}"""
      
    return string;



  def svg(self):
    size = self.bond_no + self.atom_no;
    # print(size);
    arr = [0] * size;
    #use sort
    string = header;
    # print(self.atom_no);
    
    for i in range(self.atom_no):
      atom = self.get_atom(i);
      atom = Atom(atom);
      # print( atom.__str__());
      # print(atom.svg());
      arr[i] = atom;
      # print( arr[i].element, arr[i].x, arr[i].y, arr[i].z );
   
    for i in range(self.atom_no, self.atom_no + self.bond_no):
      bond = self.get_bond(i - self.atom_no);
      bond = Bond(bond);
      # print(bond.__str__())
      arr[i] = bond
      # print( bond.a1, bond.a2, bond.epairs, bond.x1, bond.y1, bond.x2, bond.y2,bond.len, bond.dx, bond.dy );
      
    
    arr.sort(key = lambda x: x.z);

    for i in range(size):
      # print(arr[i].svg())
      string += arr[i].svg();

    return  string + footer;


  def parse(self, file):
    allLines = file.readlines();
    # lines stores the lines
    txt = allLines[3];
    # print(txt);
    var = [int(s) for s in txt.split() if s.isdigit()];
    num1 = 5 + var[0] - 1;
    num2 = num1 + var[1];
    atomLines = allLines[4:num1];
    for i in range(var[0]):
      #extract all ints and one char and append to atom
      import re
      s = atomLines[i];
      result = re.findall(r"[-+]?\d*\.\d+|\d+", s);
      elem = " ".join(re.split("[^a-zA-Z]*", atomLines[i]))
      #three resultant floats in atom
      # print(float(result[0]));
      # print(float(result[1]));
      # print(float(result[2]));
      #converting to char
      elem = ''.join(elem.split())
      # elem.strip();
      # print(elem);
      #create a string of size 3 for char arr[3]
      # string = "   ";
      # elemChar = [char for char in string];
      # for i in range(3):
      #   elemChar[i] = res1[i];
      # print(elemChar);
      #append to atom
      self.append_atom(elem, float(result[0]), float(result[1]), float(result[2]));
      
    
    # print(atomLines[0]);
    bondLines = allLines[num1:num2];
    for i in range(var[1]):
      s2 = bondLines[i];
      result = re.findall(r"[-+]?\d*\.\d+|\d+", s2);
      # print(result)
      # print(int(result[0]), end= "")
      # print(" ", end= "");
      # print(int(result[1]), end = "")
      # print(" ", end= "")
      # print(int(result[2]))
      self.append_bond(int(result[0]) - 1, int(result[1]) - 1, int(result[2]))
    # print(bondLines[0]);
  
    

    




        
    




# file = open("caffeine-3D-structure-CT1001987571.sdf");
# mol = Molecule();
# mol.parse(file);
# string = mol.svg();

# print(string);





# mol = molecule.molecule();
# mol.append_atom( "O", 2.5369, -0.1550, 0.0000 );
# mol.append_atom( "H", 3.0739, 0.1550, 0.0000 );
# mol.append_atom( "H", 2.0000, 0.1550, 0.0000 );
# atom = mol.get_atom(1);
# atom = Atom(atom);
# string = atom.__str__();
# print(string);

# moleculeClass = Molecule(mol);
# string2 = moleculeClass.__str__();
# print(string2);





