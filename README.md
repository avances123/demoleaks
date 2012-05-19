### The Idea
This project is a gis-aware app to store electoral data, it's based on Django 1.4, postgis and postgresql and the initial_data is based on the Spanish 2011 national election, but might be used with any custom coded parser which will have to align to the schema of demoleaks. It's in alfa version

### Open Data
If you think you have some electoral data to be shared with the population please use and contribute with your own parsers

### The Model
1. **Party**         Object to store party or union data
2. **Place**         Object to store an Administrative Area (MULTYPOLYGON field available)
3. **Election**      Object to store a public election (and its administrative level)
4. **Result**        Electoral data of one Place in one Election (popultation,num of voters...)
5. **ResultParties** Electoral data related of one Party in one Result

### The Documentation
See [https://github.com/avances123/demoleaks/wiki/_pages](wiki)