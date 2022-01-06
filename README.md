# MongoDB-Injection
### Cheesy Multi-threaded script for NoSQL Injection
This challenge-script is custom-made for web-server running **MongoDB** which is vulnerable to **No-SQL injection**. 

For this example:
- Underlying collection on the database contains *username* and *password* field
- Query reflects on URL and `admin' && this.password && this.password.match(/.*/)%00` payload works
- Above payload gives out list of names (eg. `admin`), if the regex pattern matches

## How this script works?
1. Find the length of password using pattern `(/./)`,`(/../)`,`(/.../)` and so on..
2. Find the password from the pre-defined charset by brute-forcing every character like `(/^{}/)`
  
  For eg. If the password is `bac`
  
  `/^a/` that will return false.
  
  `/^b/` that will return true.
  
  `/^ba/` that will return true.
  
  `/^baa/` that will return false.
  
  `/^bab/` that will return false.
  
  `/^bac/` that will return true.

3. At last the password is finally confirmed with regex `(/^{}$/)`
 
## How to use?
Just provide values to these variables for your use:

- ***URL*** (URL for the web-server)

- ***Field*** (Field on the collection to inject on)

- ***Flag*** (String which contains the unique success result on injection)

Some **Optional** values are:
- *Password* (A part of field value)

- *Requests/sec* (Default:10)   

- *Password Max length* (Default:50)

- *Password length* (Exact field length)
