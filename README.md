## Installation
          
Navigate to your directory of choice the proceed as follows;<br>
          
### 1 .Clone the git repo and create a virtual environment 
          
Depending on your operating system,make a virtual environment to avoid messing with your machine's primary dependencies
          
> **Windows**
          
```
git clone https://github.com/Dev-Elie/GDSC_MUT-WEB-Series.git .
cd your-working-directory
py -3 -m venv venv
```
          
> **macOS/Linux**
          
```
git clone https://github.com/Dev-Elie/GDSC_MUT-WEB-Series.git .
cd your-working-directory
py -3 -m venv venv
```

### 2 .Activate the virtual environment (venv)
          
> **Windows** 

```venv\Scripts\activate```
          
> **macOS/Linux**

```. venv/bin/activate```
or
```source venv/bin/activate```

### 3 .Install the requirements

Applies for windows/macOS/Linux

```pip install -r requirements.txt```

### 4. Run the application 

> **For linux and macOS**
Make the run file executable by running the code

```chmod 777 run```

Then start the application by executing the run file

```./run```

> **On windows**
```
set FLASK_APP=main
flask run
```

If you choose to start on a new database, delete the *migrations* directory and the *database.db* file then on your terminal ( make sure you're in the correct working directory) then run;

### 1. Create a migration repository

`flask db init`

> Creates a new migrations folder inside your cwd.

### 2. Generate an initial migration

`flask db migrate`

> Creates a database with the required table.

### 3. Apply the migration to the database

`flask db upgrade`

Then, whenever the database models change, run the migrate and upgrade commands again.



