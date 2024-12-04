CREATE TABLE [dbo].[weather_table](
	[Ciudad] [nvarchar](100) NULL,
	[Temperatura] [decimal](5, 2) NULL,
	[Descripcion] [nvarchar](255) NULL,
	[Humedad] [int] NULL,
	[Viento] [decimal](5, 2) NULL,
	[Presion] [int] NULL,
	[Latitud] [decimal](9, 6) NULL,
	[Longitud] [decimal](9, 6) NULL
) ON [PRIMARY]
GO