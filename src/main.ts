import { ValidationPipe } from '@nestjs/common';
import { NestFactory } from '@nestjs/core';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Configuração global de prefixo da API
  app.setGlobalPrefix('api/v1');

  // Configuração de CORS
  app.enableCors({
    origin: process.env.CORS_ORIGIN || '*',
    methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
    credentials: true,
  });

  // Configuração global de validação
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true, // Remove propriedades não decoradas
      transform: true, // Transforma tipos automaticamente
      forbidNonWhitelisted: true, // Rejeita propriedades não decoradas
      transformOptions: {
        enableImplicitConversion: true, // Converte tipos implicitamente
      },
    }),
  );

  // Configuração do Swagger
  const config = new DocumentBuilder()
    .setTitle('API Biblioteca')
    .setVersion('1.0')
    .addBearerAuth(
      {
        type: 'http',
        scheme: 'bearer',
        bearerFormat: 'JWT',
        name: 'JWT',
        description: 'Insira o token JWT',
        in: 'header',
      },
      'JWT-auth',
    )
    .addTag('Gestão de Alunos', 'Endpoints para gerenciamento de alunos')
    .addTag('Gestão de Livros', 'Endpoints para gerenciamento de livros')
    .addTag('Gestão de Empréstimos', 'Endpoints para gerenciamento de empréstimos')
    .build();

  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('docs', app, document, {
    swaggerOptions: {
      persistAuthorization: true,
      tagsSorter: 'alpha',
      operationsSorter: 'alpha',
    },
    customSiteTitle: 'API Biblioteca - Documentação',
  });

  // Configuração da porta
  const port = process.env.PORT || 3000;
  await app.listen(port);
}
bootstrap();
