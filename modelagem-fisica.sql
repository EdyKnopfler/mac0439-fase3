CREATE FUNCTION criarstatusparanovorequisito() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
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
$$;


CREATE FUNCTION criarstatusparatodosrequisitos() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
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
$$;


CREATE TABLE anuncio_doacao (
    id integer NOT NULL,
    data_hora timestamp with time zone NOT NULL,
    data_inicio date NOT NULL,
    data_termino date NOT NULL,
    status character varying(10) NOT NULL,
    id_mongo character varying(24),
    escolhido_id integer,
    pet_id integer NOT NULL
);


CREATE SEQUENCE anuncio_doacao_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE anuncio_doacao_id_seq OWNED BY anuncio_doacao.id;


CREATE TABLE django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


CREATE SEQUENCE django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


CREATE TABLE foto (
    id integer NOT NULL,
    arquivo character varying(100) NOT NULL,
    pet_id integer NOT NULL
);


CREATE SEQUENCE foto_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE foto_id_seq OWNED BY foto.id;


CREATE TABLE marcado_no_post (
    id integer NOT NULL,
    post_id integer NOT NULL,
    usuario_id integer NOT NULL
);


CREATE SEQUENCE marcado_no_post_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE marcado_no_post_id_seq OWNED BY marcado_no_post.id;


CREATE TABLE pessoa_fisica (
    usuario_ptr_id integer NOT NULL,
    cpf character varying(11) NOT NULL,
    data_nascimento date
);


CREATE TABLE pessoa_juridica (
    usuario_ptr_id integer NOT NULL,
    cnpj character varying(14) NOT NULL
);


CREATE TABLE pet (
    id integer NOT NULL,
    nome character varying(80) NOT NULL,
    especie character varying(80) NOT NULL,
    data_nascimento date,
    id_mongo character varying(24),
    dono_id integer NOT NULL
);


CREATE SEQUENCE pet_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE pet_id_seq OWNED BY pet.id;


CREATE TABLE post (
    id integer NOT NULL,
    data_hora timestamp with time zone NOT NULL,
    titulo character varying(80) NOT NULL,
    id_mongo character varying(24),
    arquivo character varying(100) NOT NULL,
    video boolean NOT NULL,
    usuario_id integer NOT NULL
);


CREATE SEQUENCE post_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE post_id_seq OWNED BY post.id;


CREATE TABLE processo_doacao (
    id integer NOT NULL,
    data_inicio date NOT NULL,
    data_termino date NOT NULL,
    anuncio_id integer NOT NULL,
    candidato_id integer NOT NULL
);


CREATE SEQUENCE processo_doacao_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE processo_doacao_id_seq OWNED BY processo_doacao.id;


CREATE TABLE requisito (
    id integer NOT NULL,
    titulo character varying(80) NOT NULL,
    id_mongo character varying(24),
    tipo character varying(11) NOT NULL,
    peso integer,
    anuncio_id integer NOT NULL
);


CREATE SEQUENCE requisito_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE requisito_id_seq OWNED BY requisito.id;


CREATE TABLE status_requisito (
    id integer NOT NULL,
    titulo character varying(80) NOT NULL,
    status character varying(12) NOT NULL,
    anuncio_id integer NOT NULL,
    candidato_id integer NOT NULL
);


CREATE SEQUENCE status_requisito_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE status_requisito_id_seq OWNED BY status_requisito.id;


CREATE TABLE usuario (
    id integer NOT NULL,
    email character varying(80) NOT NULL,
    senha character varying(20) NOT NULL,
    nome character varying(80) NOT NULL,
    rua character varying(80),
    bairro character varying(80),
    cidade character varying(80),
    estado character varying(2),
    cep character varying(8),
    telefone character varying(11),
    latitude double precision,
    longitude double precision,
    id_mongo character varying(24),
    tipo character varying(2) NOT NULL
);


CREATE SEQUENCE usuario_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE usuario_id_seq OWNED BY usuario.id;


CREATE TABLE visita (
    id integer NOT NULL,
    data_hora timestamp with time zone NOT NULL,
    comentario character varying(200) NOT NULL,
    pet_id integer NOT NULL,
    visitante_id integer NOT NULL
);


CREATE SEQUENCE visita_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE visita_id_seq OWNED BY visita.id;


ALTER TABLE ONLY anuncio_doacao ALTER COLUMN id SET DEFAULT nextval('anuncio_doacao_id_seq'::regclass);
ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);
ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);
ALTER TABLE ONLY foto ALTER COLUMN id SET DEFAULT nextval('foto_id_seq'::regclass);
ALTER TABLE ONLY marcado_no_post ALTER COLUMN id SET DEFAULT nextval('marcado_no_post_id_seq'::regclass);
ALTER TABLE ONLY pet ALTER COLUMN id SET DEFAULT nextval('pet_id_seq'::regclass);
ALTER TABLE ONLY post ALTER COLUMN id SET DEFAULT nextval('post_id_seq'::regclass);
ALTER TABLE ONLY processo_doacao ALTER COLUMN id SET DEFAULT nextval('processo_doacao_id_seq'::regclass);
ALTER TABLE ONLY requisito ALTER COLUMN id SET DEFAULT nextval('requisito_id_seq'::regclass);
ALTER TABLE ONLY status_requisito ALTER COLUMN id SET DEFAULT nextval('status_requisito_id_seq'::regclass);
ALTER TABLE ONLY usuario ALTER COLUMN id SET DEFAULT nextval('usuario_id_seq'::regclass);
ALTER TABLE ONLY visita ALTER COLUMN id SET DEFAULT nextval('visita_id_seq'::regclass);


ALTER TABLE ONLY anuncio_doacao
    ADD CONSTRAINT anuncio_doacao_pkey PRIMARY KEY (id);

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);

ALTER TABLE ONLY foto
    ADD CONSTRAINT foto_pkey PRIMARY KEY (id);

ALTER TABLE ONLY marcado_no_post
    ADD CONSTRAINT marcado_no_post_pkey PRIMARY KEY (id);

ALTER TABLE ONLY pessoa_fisica
    ADD CONSTRAINT pessoa_fisica_cpf_key UNIQUE (cpf);

ALTER TABLE ONLY pessoa_fisica
    ADD CONSTRAINT pessoa_fisica_pkey PRIMARY KEY (usuario_ptr_id);


ALTER TABLE ONLY pessoa_juridica
    ADD CONSTRAINT pessoa_juridica_cnpj_key UNIQUE (cnpj);

ALTER TABLE ONLY pessoa_juridica
    ADD CONSTRAINT pessoa_juridica_pkey PRIMARY KEY (usuario_ptr_id);

ALTER TABLE ONLY pet
    ADD CONSTRAINT pet_pkey PRIMARY KEY (id);

ALTER TABLE ONLY post
    ADD CONSTRAINT post_pkey PRIMARY KEY (id);

ALTER TABLE ONLY processo_doacao
    ADD CONSTRAINT processo_doacao_anuncio_id_candidato_id_26b323e4_uniq UNIQUE (anuncio_id, candidato_id);

ALTER TABLE ONLY processo_doacao
    ADD CONSTRAINT processo_doacao_pkey PRIMARY KEY (id);

ALTER TABLE ONLY requisito
    ADD CONSTRAINT requisito_anuncio_id_titulo_52ea075b_uniq UNIQUE (anuncio_id, titulo);

ALTER TABLE ONLY requisito
    ADD CONSTRAINT requisito_pkey PRIMARY KEY (id);

ALTER TABLE ONLY status_requisito
    ADD CONSTRAINT status_requisito_anuncio_id_candidato_id_titulo_3c12e9d5_uniq UNIQUE (anuncio_id, candidato_id, titulo);

ALTER TABLE ONLY status_requisito
    ADD CONSTRAINT status_requisito_pkey PRIMARY KEY (id);

ALTER TABLE ONLY usuario
    ADD CONSTRAINT usuario_email_key UNIQUE (email);

ALTER TABLE ONLY usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id);

ALTER TABLE ONLY visita
    ADD CONSTRAINT visita_pkey PRIMARY KEY (id);

CREATE INDEX anuncio_doacao_escolhido_id_6c1ebd0c ON anuncio_doacao USING btree (escolhido_id);

CREATE INDEX anuncio_doacao_pet_id_4343cde3 ON anuncio_doacao USING btree (pet_id);

CREATE INDEX django_session_expire_date_a5c62663 ON django_session USING btree (expire_date);

CREATE INDEX django_session_session_key_c0390e0f_like ON django_session USING btree (session_key varchar_pattern_ops);

CREATE INDEX foto_pet_id_cdbcd7d6 ON foto USING btree (pet_id);

CREATE INDEX marcado_no_post_post_id_c10d2bd3 ON marcado_no_post USING btree (post_id);

CREATE INDEX marcado_no_post_usuario_id_142b04e3 ON marcado_no_post USING btree (usuario_id);

CREATE INDEX pessoa_fisica_cpf_09bec132_like ON pessoa_fisica USING btree (cpf varchar_pattern_ops);

CREATE INDEX pessoa_juridica_cnpj_a01a9de6_like ON pessoa_juridica USING btree (cnpj varchar_pattern_ops);

CREATE INDEX pet_dono_id_c971f5d5 ON pet USING btree (dono_id);

CREATE INDEX post_usuario_id_70e491e0 ON post USING btree (usuario_id);

CREATE INDEX processo_doacao_anuncio_id_d8438acb ON processo_doacao USING btree (anuncio_id);

CREATE INDEX processo_doacao_candidato_id_49adbc09 ON processo_doacao USING btree (candidato_id);

CREATE INDEX requisito_anuncio_id_439be220 ON requisito USING btree (anuncio_id);

CREATE INDEX status_requisito_anuncio_id_00a8b04f ON status_requisito USING btree (anuncio_id);

CREATE INDEX status_requisito_candidato_id_df88369c ON status_requisito USING btree (candidato_id);

CREATE INDEX usuario_email_de9343f9_like ON usuario USING btree (email varchar_pattern_ops);

CREATE INDEX visita_pet_id_b6fa994b ON visita USING btree (pet_id);

CREATE INDEX visita_visitante_id_9f92cdb6 ON visita USING btree (visitante_id);

CREATE TRIGGER inserirstatusnovorequisito AFTER INSERT ON requisito FOR EACH ROW EXECUTE PROCEDURE criarstatusparanovorequisito();

CREATE TRIGGER inserirstatustodosrequisitos AFTER INSERT ON processo_doacao FOR EACH ROW EXECUTE PROCEDURE criarstatusparatodosrequisitos();

ALTER TABLE ONLY anuncio_doacao
    ADD CONSTRAINT anuncio_doacao_escolhido_id_6c1ebd0c_fk_usuario_id FOREIGN KEY (escolhido_id) REFERENCES usuario(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY anuncio_doacao
    ADD CONSTRAINT anuncio_doacao_pet_id_4343cde3_fk_pet_id FOREIGN KEY (pet_id) REFERENCES pet(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY foto
    ADD CONSTRAINT foto_pet_id_cdbcd7d6_fk_pet_id FOREIGN KEY (pet_id) REFERENCES pet(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY marcado_no_post
    ADD CONSTRAINT marcado_no_post_post_id_c10d2bd3_fk_post_id FOREIGN KEY (post_id) REFERENCES post(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY marcado_no_post
    ADD CONSTRAINT marcado_no_post_usuario_id_142b04e3_fk_usuario_id FOREIGN KEY (usuario_id) REFERENCES usuario(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY pessoa_fisica
    ADD CONSTRAINT pessoa_fisica_usuario_ptr_id_5ec0f86d_fk_usuario_id FOREIGN KEY (usuario_ptr_id) REFERENCES usuario(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY pessoa_juridica
    ADD CONSTRAINT pessoa_juridica_usuario_ptr_id_a12d07a4_fk_usuario_id FOREIGN KEY (usuario_ptr_id) REFERENCES usuario(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY pet
    ADD CONSTRAINT pet_dono_id_c971f5d5_fk_usuario_id FOREIGN KEY (dono_id) REFERENCES usuario(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY post
    ADD CONSTRAINT post_usuario_id_70e491e0_fk_usuario_id FOREIGN KEY (usuario_id) REFERENCES usuario(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY processo_doacao
    ADD CONSTRAINT processo_doacao_anuncio_id_d8438acb_fk_anuncio_doacao_id FOREIGN KEY (anuncio_id) REFERENCES anuncio_doacao(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY processo_doacao
    ADD CONSTRAINT processo_doacao_candidato_id_49adbc09_fk_usuario_id FOREIGN KEY (candidato_id) REFERENCES usuario(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY requisito
    ADD CONSTRAINT requisito_anuncio_id_439be220_fk_anuncio_doacao_id FOREIGN KEY (anuncio_id) REFERENCES anuncio_doacao(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY status_requisito
    ADD CONSTRAINT status_requisito_anuncio_id_00a8b04f_fk_anuncio_doacao_id FOREIGN KEY (anuncio_id) REFERENCES anuncio_doacao(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY status_requisito
    ADD CONSTRAINT status_requisito_anuncio_id_fkey FOREIGN KEY (anuncio_id, titulo) REFERENCES requisito(anuncio_id, titulo) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY status_requisito
    ADD CONSTRAINT status_requisito_anuncio_id_fkey1 FOREIGN KEY (anuncio_id, candidato_id) REFERENCES processo_doacao(anuncio_id, candidato_id) ON DELETE CASCADE;

ALTER TABLE ONLY status_requisito
    ADD CONSTRAINT status_requisito_candidato_id_df88369c_fk_usuario_id FOREIGN KEY (candidato_id) REFERENCES usuario(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY visita
    ADD CONSTRAINT visita_pet_id_b6fa994b_fk_pet_id FOREIGN KEY (pet_id) REFERENCES pet(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY visita
    ADD CONSTRAINT visita_visitante_id_9f92cdb6_fk_usuario_id FOREIGN KEY (visitante_id) REFERENCES usuario(id) DEFERRABLE INITIALLY DEFERRED;

