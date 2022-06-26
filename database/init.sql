CREATE TABLE public.url_table (
    id SERIAL PRIMARY KEY,
    original_url VARCHAR,
    shortened_url VARCHAR(255),
    creation_date TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('UTC', NOW())
);

CREATE UNIQUE INDEX original_url_index ON public.url_table(original_url)