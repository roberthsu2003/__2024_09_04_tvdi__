CREATE TABLE public.site_info (
	編號 varchar(50) NOT NULL,
	站點名稱 varchar(50) NOT NULL,
	行政區 varchar(10) NOT NULL,
	地址 varchar(50) NULL,
	緯度 float8 NULL,
	經度 float8 NULL,
	CONSTRAINT site_info_unique UNIQUE ("站點名稱"),
	CONSTRAINT site_info_unique_1 UNIQUE ("行政區"),
	CONSTRAINT youbike_site_pk PRIMARY KEY ("編號")
);