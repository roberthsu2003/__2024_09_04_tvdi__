CREATE TABLE IF NOT EXISTS public.user(
	user_id SERIAL PRIMARY KEY,
	user_name varchar(50) NOT NULL,
	user_email varchar(50) NOT NULL,
	password varchar(100) NOT NULL,
	UNIQUE(user_email)
);

SELECT count(*) 
FROM  public.user
WHERE user_email = 'roberthsu2003@gmail.com';

INSERT INTO public.USER(user_name,user_email,password)
VALUES ('robert','robert_hsu2003','12345');

DELETE FROM public.user;

DROP TABLE public.user;

SELECT user_name,password
FROM public.USER
WHERE user_email='roberthsu2003@gmail.com'




