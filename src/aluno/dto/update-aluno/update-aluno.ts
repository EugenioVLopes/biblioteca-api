import { PartialType } from '@nestjs/swagger';
import { CreateAlunoDto } from '../create-aluno/create-aluno';

export class UpdateAlunoDto extends PartialType(CreateAlunoDto) {}
