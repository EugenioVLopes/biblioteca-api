import { ApiProperty } from '@nestjs/swagger';
import { IsEmail, IsNotEmpty, IsNumber, IsString } from 'class-validator';

export class CreateAlunoDto {
  @ApiProperty({ example: 2022001234, description: 'Matrícula única do aluno' })
  @IsNumber()
  mat: number;

  @ApiProperty({ example: 'Maria Silva', description: 'Nome completo do aluno' })
  @IsString()
  @IsNotEmpty()
  nome: string;

  @ApiProperty({ example: 'maria@email.com', description: 'E-mail institucional do aluno' })
  @IsEmail()
  email: string;

  @ApiProperty({ example: 'Sistemas de Informação', description: 'Curso no qual o aluno está matriculado' })
  @IsString()
  @IsNotEmpty()
  curso: string;
}
