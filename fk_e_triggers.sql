-- Ao criar um *Processo de Doação*, 
-- criar também *Status de Requisito* 
-- para todos os *Requisitos* no *Anúncio*
create or replace function CriarStatusParaTodosRequisitos()
returns trigger as $$
declare
   req record;
begin
   for req in
      select * from requisito
      where anuncio_id = new.anuncio_id
   loop
      insert into status_requisito
          (titulo, status, anuncio_id, candidato_id)
      values
          (req.titulo, 'a verificar', new.anuncio_id, new.candidato_id);
   end loop;
   return new;
end;
$$ language plpgsql;

drop trigger if exists InserirStatusTodosRequisitos ON processo_doacao;

create trigger InserirStatusTodosRequisitos
after insert on processo_doacao
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
      select * from processo_doacao
      where anuncio_id = new.anuncio_id
   loop
      insert into status_requisito
          (titulo, status, anuncio_id, candidato_id)
      values
          (new.titulo, 'a verificar', new.anuncio_id, processo.candidato_id);
   end loop;
   return new;
end;
$$ language plpgsql;

drop trigger if exists InserirStatusNovoRequisito ON requisito;

create trigger InserirStatusNovoRequisito
after insert on requisito
for each row
execute procedure CriarStatusParaNovoRequisito();

-- Ao excluir um *Requisito*
-- excluir também todos os *Status de Requisito*
alter table status_requisito
add foreign key(anuncio_id, titulo) 
references requisito(anuncio_id, titulo) ON DELETE CASCADE ON UPDATE CASCADE;

-- Ao excluir um *Processo de Doação*
-- excluir também todos os *Status de Requisitos*
alter table status_requisito
add foreign key(anuncio_id, candidato_id) 
references processo_doacao(anuncio_id, candidato_id) ON DELETE CASCADE;

