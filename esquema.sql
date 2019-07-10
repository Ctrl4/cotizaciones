CREATE TABLE monedas (
	id	serial primary key,
	moneda	varchar(20) not null,
	compra float,
	venta float,
	fecha_actualizacion timestamp default current_timestamp
);
