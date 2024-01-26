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
	created_at	timestamp,
	last_update timestamp
)
server airtable_server
options (
  base_id 'appAyg77fwZrSZShX',
  table_id 'tblOXn0lWpf4gTjFz',
  rowid_column 'article_id'
);
