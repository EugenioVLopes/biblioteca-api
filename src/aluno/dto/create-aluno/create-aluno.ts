import { ApiProperty } from '@nestjs/swagger';
import { IsEmail, IsNotEmpty, IsNumber, IsString, MaxLength, MinLength } from 'class-validator';

export class CreateAlunoDto {
  @ApiProperty({
    example: 2022001234,
    description: 'Matrícula única do aluno',
    minimum: 1000000000,
    maximum: 9999999999,
  })
  @IsNumber()
  mat: number;

  @ApiProperty({
    example: 'Maria Silva',
    description: 'Nome completo do aluno',
    minLength: 3,
    maxLength: 100,
  })
  @IsString()
  @IsNotEmpty()
  @MinLength(3)
  @MaxLength(100)
  nome: string;

  @ApiProperty({
    example: 'maria@email.com',
    description: 'E-mail institucional do aluno',
    format: 'email',
  })
  @IsEmail()
  email: string;

  @ApiProperty({
    example: 'Sistemas de Informação',
    description: 'Curso no qual o aluno está matriculado',
    minLength: 3,
    maxLength: 100,
  })
  @IsString()
  @IsNotEmpty()
  @MinLength(3)
  @MaxLength(100)
  curso: string;
}
