create extension if not exists wrappers with schema extensions;

create foreign data wrapper airtable_wrapper
  handler airtable_fdw_handler
  validator airtable_fdw_validator;

-- drop server airtable_server cascade;

create server airtable_server
  foreign data wrapper airtable_wrapper
  options (
    api_url 'https://api.airtable.com/v0',  -- Airtable API url, optional
    api_key ''  -- Airtable API key or Personal Access Token (PAT), required
  );

create foreign table airtable_articles (
  	article_id	int4,
	url	text,
  email text,
	created_at	timestamp,
	last_update timestamp
)
server airtable_server
options (
  base_id 'appAyg77fwZrSZShX',
  table_id 'tblOXn0lWpf4gTjFz',
  rowid_column 'article_id'
);


create table public.articles_summary (
    summary_id serial primary key,
    summary text not null,
    dependencies json not null,
    created_at timestamp not null default now()
);

create table public.processed_articles (
    article_id int primary key,
    url text not null,
    content text not null,
    summary text not null,
    created_at timestamp not null default now(),
    reprocess boolean not null default true
);