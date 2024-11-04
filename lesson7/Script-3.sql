/*選擇站點名稱*/
SELECT DISTINCT sitename
FROM records

SELECT date,county,aqi,pm25,status,lat,lon
FROM records
WHERE sitename='富貴角'
ORDER BY date DESC;

