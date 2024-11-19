SELECT  count(*)
FROM records;

SELECT date,aqi,pm25
FROM records
WHERE sitename = '大城';