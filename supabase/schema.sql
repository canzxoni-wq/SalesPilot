Claude



























Schema · SQL
-- SalesPilot: archivio delle ricerche con account individuali.
-- Eseguire una sola volta nel SQL Editor di Supabase (si può rieseguire senza danni).
 
create table if not exists public.salespilot_searches (
  id          text primary key,
  user_id     uuid not null default auth.uid() references auth.users(id) on delete cascade,
  payload     jsonb not null,
  created_at  timestamptz not null default now()
);
 
-- Se la tabella esisteva già (versione con chiave service_role, senza utenti),
-- aggiunge le colonne mancanti senza toccare i dati presenti.
alter table public.salespilot_searches
  add column if not exists user_id uuid references auth.users(id) on delete cascade;
alter table public.salespilot_searches
  alter column user_id set default auth.uid();
alter table public.salespilot_searches
  add column if not exists created_at timestamptz not null default now();
-- Le eventuali ricerche già salvate senza utente restano nel database ma non
-- sono visibili a nessuno. Per assegnarle a un account:
--   update public.salespilot_searches set user_id = '<id utente da Authentication>' where user_id is null;
 
create index if not exists salespilot_searches_user_created_idx
  on public.salespilot_searches (user_id, created_at desc);
 
-- Row Level Security: ogni utente legge, crea, modifica e cancella solo le proprie ricerche.
alter table public.salespilot_searches enable row level security;
 
drop policy if exists "salespilot_select_own" on public.salespilot_searches;
drop policy if exists "salespilot_insert_own" on public.salespilot_searches;
drop policy if exists "salespilot_update_own" on public.salespilot_searches;
drop policy if exists "salespilot_delete_own" on public.salespilot_searches;
 
create policy "salespilot_select_own" on public.salespilot_searches
  for select to authenticated using (auth.uid() = user_id);
create policy "salespilot_insert_own" on public.salespilot_searches
  for insert to authenticated with check (auth.uid() = user_id);
create policy "salespilot_update_own" on public.salespilot_searches
  for update to authenticated using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "salespilot_delete_own" on public.salespilot_searches
  for delete to authenticated using (auth.uid() = user_id);
 
-- Medie dei feedback dell'utente loggato. security_invoker = la vista rispetta la RLS.
drop view if exists public.salespilot_feedback_stats;
create view public.salespilot_feedback_stats
with (security_invoker = true) as
select
  count(*) filter (where payload ? 'feedback')                     as numero_feedback,
  round(avg((payload -> 'feedback' ->> 'aziende')::numeric), 2)    as media_aziende,
  round(avg((payload -> 'feedback' ->> 'dati')::numeric), 2)       as media_dati,
  round(avg((payload -> 'feedback' ->> 'utilita')::numeric), 2)    as media_utilita
from public.salespilot_searches;
 
revoke all on public.salespilot_searches from anon;
revoke all on public.salespilot_feedback_stats from anon;
grant select, insert, update, delete on public.salespilot_searches to authenticated;
grant select on public.salespilot_feedback_stats to authenticated;
 
Claude ha terminato la risposta
