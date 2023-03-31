import os;
import sqlite3;
import MolDisplay;
# import molecule;


class Database:
    
    def __init__( self, reset=False ):
      if(reset == True):
       if os.path.exists( 'molecules.db' ):
        os.remove( 'molecules.db' );
      self.conn = sqlite3.connect( 'molecules.db' );
      
    def create_tables( self ):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS Elements(
            ELEMENT_NO          INTEGER NOT NULL,
            ELEMENT_CODE        VARCHAR(3) NOT NULL PRIMARY KEY,
            ELEMENT_NAME        VARCHAR(32) NOT NULL,
            COLOUR1             CHAR(6) NOT NULL,
            COLOUR2             CHAR(6) NOT NULL,
            COLOUR3             CHAR(6) NOT NULL,
            RADIUS              DECIMAL(3) NOT NULL
            );''');

        self.conn.execute("""CREATE TABLE IF NOT EXISTS Atoms(
            ATOM_ID             INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            ELEMENT_CODE        VARCHAR(3) NOT NULL,
            X DECIMAL(7,4)      NOT NULL,
            Y DECIMAL(7,4)      NOT NULL,
            Z DECIMAL(7,4)      NOT NULL,
            FOREIGN KEY (ELEMENT_CODE) REFERENCES Elements(ELEMENT_CODE))""");
        

        self.conn.execute("""CREATE TABLE IF NOT EXISTS Bonds(
            BOND_ID             INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            A1                  INTEGER NOT NULL,
            A2                  INTEGER NOT NULL,
            EPAIRS              INTEGER NOT NULL);""");

        self.conn.execute("""CREATE TABLE IF NOT EXISTS Molecules(
            MOLECULE_ID         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            NAME                TEXT NOT NULL UNIQUE);""");

        self.conn.execute("""CREATE TABLE IF NOT EXISTS MoleculeAtom(
            MOLECULE_ID         INTEGER NOT NULL,
            ATOM_ID             INTEGER NOT NULL,
            PRIMARY KEY (MOLECULE_ID, ATOM_ID),
            FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules(MOLECULE_ID),
            FOREIGN KEY (ATOM_ID) REFERENCES Atoms(ATOM_ID));""");

        self.conn.execute("""CREATE TABLE IF NOT EXISTS MoleculeBond(
            MOLECULE_ID         INTEGER NOT NULL,
            BOND_ID             INTEGER NOT NULL,
            PRIMARY KEY (MOLECULE_ID, BOND_ID),
            FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules(MOLECULE_ID),
            FOREIGN KEY (BOND_ID) REFERENCES Bonds(BOND_ID))""");
        
    
    
    def __setitem__( self, table, values ):
       length = len(values);
       string = "(" + ",".join(["?"] * length) + ")";
       self.conn.execute(f"INSERT INTO {table} VALUES {string}", values);
    


    def deleteItem( self, values):
       cursor = self.conn.cursor()
       query =  """DELETE FROM Elements WHERE ELEMENT_CODE = ( ? );""" ;
       params = (values)
       cursor.execute(query, params)


    def checkItem( self, values):
       cursor = self.conn.cursor()
       query =  """SELECT 
                    ELEMENT_CODE
                    FROM Elements
                    WHERE ELEMENT_CODE = ( ? );""" ;
       params = (values)
       cursor.execute(query, params)
       molID = cursor.fetchone()
       if(molID is None):
          return False;
          
       if(molID[0] == values):
          return True;
       else:
          return False;
    
    
    
    def add_atom( self, molname, atom ):
       cursor = self.conn.cursor()
       query =  """INSERT
                INTO   Atoms  ( ELEMENT_CODE,   X,        Y,           Z )
                VALUES        ( ?,              ?,          ?,          ?);""" ;
       params = (atom.atom.element, atom.atom.x, atom.atom.y, atom.z)
       cursor.execute(query, params)
       atom_id = cursor.lastrowid
    #    print(molname);
       query2 =  """SELECT 
                    MOLECULE_ID
                    FROM Molecules
                    WHERE NAME = ( ? );""" ;
       params2 = (molname);
       data_id = cursor.execute(query2, (params2,));
       molID = cursor.fetchone()[0]
    #    print(molID);
    #    print(data_id);
    #    if(data is None):
    #         query = "INSERT OR REPLACE INTO Molecules (NAME) VALUES (?)";
    #         cursor.execute(query, (molname,))
       self.conn.execute( f"""INSERT
                INTO   MoleculeAtom  (MOLECULE_ID, ATOM_ID)
                VALUES               (   {molID},    {atom_id}    );""");


    def add_bond( self, molname, bond ):
        cursor = self.conn.cursor();
        query =  """INSERT
                    INTO   Bonds  ( A1,        A2,           EPAIRS )
                    VALUES        (  ?,          ?,          ?);""" ;
        params = (bond.bond.a1, bond.bond.a2, bond.bond.epairs);
        cursor.execute(query, params);
        bond_id = cursor.lastrowid
        #    print(atom_id);
        # self.conn.execute(f"SELECT MOLECULE_ID FROM Molecules WHERE NAME = '{molname}'");
        # data = cursor.fetchone();
        #    print(data);
        # if(cursor.fetchone() is None):
        #         query = "INSERT INTO Molecules (NAME) VALUES (?)";
        #         cursor.execute(query, (molname,))     
        query2 =  """SELECT 
                    MOLECULE_ID
                    FROM Molecules
                    WHERE NAME = ( ? );""" ;
        params2 = (molname);
        data_id = cursor.execute(query2, (params2,));
        molID = cursor.fetchone()[0]
    #    print(molID);
    #    print(data_id);
    #    if(data is None):
    #         query = "INSERT OR REPLACE INTO Molecules (NAME) VALUES (?)";
    #         cursor.execute(query, (molname,))
        self.conn.execute( f"""INSERT
                    INTO   MoleculeBond  (MOLECULE_ID, BOND_ID)
                    VALUES               (   {molID},    {bond_id}    );""");


    def add_molecule( self, name, fp ):
        cursor = self.conn.cursor();
        mol = MolDisplay.Molecule();
        mol.parse(fp);
        query =  """INSERT
                    INTO   Molecules  (NAME)
                    VALUES            ( ? );""" ;
        params = (name);
        cursor.execute(query, (params,));
        for i in range(mol.atom_no):
            self.add_atom(name, MolDisplay.Atom(mol.get_atom(i)));

        for i in range(mol.bond_no):
            self.add_bond(name, MolDisplay.Bond(mol.get_bond(i)));


    def load_mol( self, name ):
       cursor = self.conn.cursor();
       mol = MolDisplay.Molecule();
       #atoms
       query =  """
        select a.ELEMENT_CODE, a.X, a.Y, a.Z
        from Molecules d
        inner join MoleculeAtom u
        on d.MOLECULE_ID = u.MOLECULE_ID
        inner join Atoms a
        on u.Atom_ID = a.ATOM_ID
        where d.NAME = (?);""" ;
       params = (name);
       cursor.execute(query, (params,));
       data = cursor.fetchall();
       for i in range(len(data)):
         mol.append_atom(data[i][0], float(data[i][1]), float(data[i][2]), float(data[i][3]));
       
       
       #bonds
       query =  """
        select a.A1, a.A2, a.EPAIRS
        from Molecules d
        inner join MoleculeBond u
        on d.MOLECULE_ID = u.MOLECULE_ID
        inner join Bonds a
        on u.BOND_ID = a.BOND_ID
        where d.NAME = (?);""" ;
       params = (name);
       cursor.execute(query, (params,));
       data2 = cursor.fetchall();
       for i in range(len(data2)):
          mol.append_bond(int(data2[i][0]), int(data2[i][1]), int(data2[i][2]));

       return mol;
       


    def radius( self ):
        cursor = self.conn.cursor();
        cursor.execute("SELECT ELEMENT_CODE, RADIUS FROM Elements")
        result_set = cursor.fetchall()
        radius_dic = {row[0]: row[1] for row in result_set}
        return radius_dic;
            
    def element_name( self ):
        cursor = self.conn.cursor();
        cursor.execute("SELECT ELEMENT_CODE, ELEMENT_NAME FROM Elements")
        result_set = cursor.fetchall()
        elemName_dic = {row[0]: row[1] for row in result_set}
        return elemName_dic;

    def radial_gradients( self ):
        cursor = self.conn.cursor();
        radialGradientSVG = "";
        data = (cursor.execute("SELECT * FROM Elements;" ).fetchall());
        for i in range(len(data)):
           radialGradientSVG += """
            <radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
                <stop offset="0%%" stop-color="#%s"/>
                <stop offset="50%%" stop-color="#%s"/>
                <stop offset="100%%" stop-color="#%s"/>
            </radialGradient>""" % (str(data[i][2]), str(data[i][3]), str(data[i][4]), str(data[i][5]));
        #    print(str(data[i][2]), str(data[i][3]), str(data[i][4]), str(data[i][5]))

        return radialGradientSVG;
           
        
        
       


if __name__ == "__main__":
    db = Database(reset=True);
    db.create_tables();
    db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 );
    db['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 );
    db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 );
    db['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40 );
    # print(db.checkItem('P'));
#     fp = open( 'water-3D-structure-CT1000292221.sdf' );
#     db.add_molecule( 'Water', fp );
#     fp = open( 'caffeine-3D-structure-CT1001987571.sdf' );
#     db.add_molecule( 'Caffeine', fp );
    # fp = open( 'CID_31260.sdf' );
    # db.add_molecule( 'Isopentanol', fp );
    # MolDisplay.radius = db.radius();
    # MolDisplay.element_name = db.element_name();
    # MolDisplay.header += db.radial_gradients();
    # for molecule in [ 'Water', 'Caffeine']:
    #     mol = db.load_mol( molecule );
        # mol.sort();
        # fp = open( molecule + ".svg", "w" );
        # fp.write( mol.svg() );
        # fp.close();
    # display tables
    # print( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() );
    # print( db.conn.execute( "SELECT * FROM Molecules;" ).fetchall() );
    # print( db.conn.execute( "SELECT * FROM Atoms;" ).fetchall() );
    # print( db.conn.execute( "SELECT * FROM Bonds;" ).fetchall() ); 
    # print( db.conn.execute( "SELECT * FROM MoleculeAtom;" ).fetchall() ); 
    # print( db.conn.execute( "SELECT * FROM MoleculeBond;" ).fetchall() );
    # radiusDic = db.radius();
    # print(radiusDic);
    # elemdic = db.element_name();
    # print(elemdic);
    # db.load_mol("Water");
    # data = db.radial_gradients();
    # print(data);

