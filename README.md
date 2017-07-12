# Open Image Dataset Maker

How to find a label and download images from the [Open Images dataset.](https://github.com/openimages/dataset)

The download script uses the multiprocessing library to speed up the download process.

### Step 1 - Find a label

Go to [google big query](https://bigquery.cloud.google.com) and use the following to find a label name

This snippet would find the desert tag, but you could also search for just a few letters to broaden the search.
```
#standardsql
SELECT
  *
FROM
  `bigquery-public-data.open_images.dict`
WHERE
  label_display_name LIKE '%desert%'
LIMIT
  200;
```

### Step 2 - Get JSON File

Once you find a tag, take note of the label_name parameter and then in a separate query run the following, after inserting the label name from the first step. 

You can also play with the confidence number if you aren't turning up enough results, or increase/decrease the limit to suit your needs.

After your search just hit the download json button to get a table of all the links.

```
#standardsql
SELECT
  i.image_id AS image_id,
  original_url,
  confidence
FROM
  `bigquery-public-data.open_images.labels` l
INNER JOIN
  `bigquery-public-data.open_images.images` i
ON
  l.image_id = i.image_id
WHERE
  label_name='/m/0284w'
  AND confidence >= 0.8
  AND Subset='train'
LIMIT
  2000;
```

### Step 3 - Download the images

Run download.py with arguments for a destination folder and the location of the json file.

`python download.py --dest myNewDataset --json myJSONFile.json`

That's it! All the files will be saved to a folder in the location that you specified. These SQL queries were pulled from [Google's OpenImage Page](https://cloud.google.com/bigquery/public-data/openimages) 
