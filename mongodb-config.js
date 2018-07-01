db.pets.createIndex({nome: "text", descricao: "text", ficha_texto: "text"});
db.anuncios.createIndex({descricao: "text"});
db.requisitos.createIndex({titulo: "text", descricao: "text"});
