Directions to Use 

Calculating_Coordinates
	1. In “input” data, rename zip code column to be “zip_code” exactly. Save as a csv. 
	2. Map the saved input zip_code file to replace the file path in “data=“ section of script. 
	3. Correct usa_ZipCodes_db filepath. All headings should be correct but check here if there’s an error.
	4. Map where you want to store the output file location and name
	5. Run


Clustering and Graphing
	1. Correct file paths for input data with latitude and longitude in separate columns
	2. Define “radius_in_miles” to define the approx size of clusters
	3. Correct “retail_locations_df” file path to be “NP_Stores_geo.csv” found in this file. If there are new stores, either manually lookup the coordinates and update this csv before running script. Or add location names and zip codes to the csv then send it through “Calculating_Coordinates.py” . 
	4. Set “threshhold_distance” in miles to define a radius to ignore when clustering from current NP locations. 
	5. Correct file path for the output csv found in “data.to_csv(“……
	6. Run