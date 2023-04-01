from http.server import HTTPServer, BaseHTTPRequestHandler;

import sys;     # to get command line argument for port
import urllib;  # code to parse for data
import io;
import molsql;
import MolDisplay;
import cgi;


# list of files that we allow the web-server to serve to clients
# (we don't want to serve any file that the client requests)
public_files = [ '/index.html', '/style.css', '/script.js', '/select.html', '/upload.html'];
database = molsql.Database(reset = True);
database.create_tables();
database['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 );
database['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 );
database['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 );
database['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40 );

class MyHandler( BaseHTTPRequestHandler ):
    def do_GET(self):

        # used to GET a file from the list ov public_files, above
        if self.path in public_files:   # make sure it's a valid file
            self.send_response( 200 );  # OK
            self.send_header( "Content-type", "text/html" );

            fp = open( self.path[1:] ); 
            # [1:] to remove leading / so that file is found in current dir

            # load the specified file
            page = fp.read();
            fp.close();

            # create and send headers
            self.send_header( "Content-length", len(page) );
            self.end_headers();

            # send the contents
            self.wfile.write( bytes( page, "utf-8" ) );

        else:
            # if the requested URL is not one of the public_files
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: not found", "utf-8" ) );



    def do_POST(self):

        if self.path == "/sdf_upload.html":
           
           #file upload

            cgi.parse_header(self.headers['Content-Type'])
            form = cgi.FieldStorage(
                fp = self.rfile,
                headers = self.headers,
                environ = {'REQUEST_METHOD': 'POST'}
            )

            # print(form);

            file_item = form['file']
            contents = file_item.file.read()
            molName = form.getvalue("molName");

            bytes_io = io.BytesIO(contents)
            file = io.TextIOWrapper(bytes_io)

            # print(file);
            database.add_molecule(molName, file);
            # print(contents)
            # print(molName)
            cursor = database.conn.cursor()

            print(cursor.execute("SELECT * FROM Molecules").fetchall());

            message = "sdf file uploaded to database";

            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/plain" );
            self.send_header( "Content-length", len(message) );
            self.end_headers();

            self.wfile.write( bytes( message, "utf-8" ) );

        elif self.path == "/form_handler.html":

            # this is specific to 'multipart/form-data' encoding used by POST
            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);

            print( repr( body.decode('utf-8') ) );

            # convert POST content into a dictionary
            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) );

            print( postvars );
            # db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 );
            if postvars['number'][0].isnumeric() and postvars['radius'][0].isnumeric() and (postvars['name'][0]).isnumeric() == False and (postvars['code'][0]).isnumeric() == False:
                if(database.checkItem(postvars['code'][0]) == False):
                  database['Elements'] = (str(postvars['number'][0]), str(postvars['code'][0]), str(postvars['name'][0]), str(postvars['c1'][0]), str(postvars['c2'][0]), str(postvars['c3'][0]), str(postvars['radius'][0]));
                  message = "Inserted into table";
                else:
                    message = "element code already exists";
            else:
                message = "incorrect values entered";



            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/plain" );
            self.send_header( "Content-length", len(message) );
            self.end_headers();

            self.wfile.write( bytes( message, "utf-8" ) );
        
        elif self.path == "/deleteElement.html":

            # this is specific to 'multipart/form-data' encoding used by POST
            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);

            print( repr( body.decode('utf-8') ) );

            # convert POST content into a dictionary
            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) );

            print( postvars );
            if(postvars['eNumber'][0].isnumeric()):
                message = "you must enter a valid element code, ex: H"
            elif len(postvars['eNumber'][0]) > 1:
                message = "you must enter a valid element code, ex: H"
            else:
                database.deleteItem(postvars['eNumber'][0]);
                message = f"Element {str(postvars['eNumber'][0])} deleted";

            dict = database.element_name();
            print(dict);

            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/plain" );
            self.send_header( "Content-length", len(message) );
            self.end_headers();

            self.wfile.write( bytes( message, "utf-8" ) );
        

        elif self.path == "/moleculesList.html":

            # this is specific to 'multipart/form-data' encoding used by POST
            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);

            print( repr( body.decode('utf-8') ) );

            # convert POST content into a dictionary
            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) );

            # print( postvars );

            cursor = database.conn.cursor()

            mols = (cursor.execute("SELECT NAME FROM Molecules").fetchall());
            string = ''
            for i in range (len(mols)):
                string += str(mols[i][0]) + ' ';
            print(string)
              
            
            message = string

            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/plain" );
            self.send_header( "Content-length", len(message) );
            self.end_headers();

            self.wfile.write( bytes( message, "utf-8" ) );
        
        elif self.path == "/display_sdf.html":

            # this is specific to 'multipart/form-data' encoding used by POST
            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);

            print( repr( body.decode('utf-8') ) );

            # convert POST content into a dictionary
            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) );
            mol_name = postvars['mol'][0]
            print(mol_name);
            MolDisplay.radius = database.radius();
            MolDisplay.element_name = database.element_name();
            MolDisplay.header += database.radial_gradients();
            mol = database.load_mol(mol_name);
            string = mol.svg();
            # mol.sort();
            # print(string);

            # cursor = database.conn.cursor()

            # mols = (cursor.execute("SELECT NAME FROM Molecules").fetchall());
            message = string

            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/plain" );
            self.send_header( "Content-length", len(message) );
            self.end_headers();

            self.wfile.write( bytes( message, "utf-8" ) );

        else:
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: not found", "utf-8" ) );




httpd = HTTPServer( ( 'localhost', 57585  ), MyHandler );
httpd.serve_forever();
