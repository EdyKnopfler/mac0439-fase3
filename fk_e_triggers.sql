-- Ao criar um *Processo de Doação*, 
-- criar também *Status de Requisito* 
-- para todos os *Requisitos* no *Anúncio*
create or replace function CriarStatusParaTodosRequisitos()
returns trigger as $$
declare
   requisito record;
begin
   for requisito in
      select * from anuncios_doacao_requisito
      where anuncio_id = new.anuncio_id
   loop
      insert into processos_doacao_statusrequisito
          (titulo, status, anuncio_id, candidato_id)
      values
          (requisito.titulo, 'a verificar', new.anuncio_id, new.candidato_id);
   end loop;
   return new;
end;
$$ language plpgsql;

drop trigger if exists InserirStatusTodosRequisitos ON processos_doacao_processodoacao;

create trigger InserirStatusTodosRequisitos
after insert on processos_doacao_processodoacao
for each row
execute procedure CriarStatusParaTodosRequisitos();

-- Ao criar um *Requisito*
-- criar também *Status de Requisito*
-- para cada *Processo de Doação* em andamento
create or replace function CriarStatusParaNovoRequisito()
returns trigger as $$
declare
   processo record;
begin
   for processo in
      select * from processos_doacao_processodoacao
      where anuncio_id = new.anuncio_id
   loop
      insert into processos_doacao_statusrequisito
          (titulo, status, anuncio_id, candidato_id)
      values
          (new.titulo, 'a verificar', new.anuncio_id, processo.candidato_id);
   end loop;
   return new;
end;
$$ language plpgsql;

drop trigger if exists InserirStatusNovoRequisito ON anuncios_doacao_requisito;

create trigger InserirStatusNovoRequisito
after insert on anuncios_doacao_requisito
for each row
execute procedure CriarStatusParaNovoRequisito();

-- Ao excluir um *Requisito*
-- excluir também todos os *Status de Requisito*
alter table processos_doacao_statusrequisito
add foreign key(anuncio_id, titulo) 
references anuncios_doacao_requisito(anuncio_id, titulo) ON DELETE CASCADE ON UPDATE CASCADE;

-- Ao excluir um *Processo de Doação*
-- excluir também todos os *Status de Requisitos*
alter table processos_doacao_statusrequisito
add foreign key(anuncio_id, candidato_id) 
references processos_doacao_processodoacao(anuncio_id, candidato_id) ON DELETE CASCADE;

