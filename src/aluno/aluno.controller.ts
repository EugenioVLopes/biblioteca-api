import { Body, Controller, Delete, Get, Param, Patch, Post } from '@nestjs/common';
import { AlunoService } from './aluno.service';

@Controller('aluno')
export class AlunoController {
  constructor(private readonly alunoService: AlunoService) {}

  @Post()
  create(@Body() data: any) {
    return this.alunoService.create(data);
  }

  @Get()
  findAll() {
    return this.alunoService.findAll();
  }

  @Get(':mat')
  findOne(@Param('mat') mat: string) {
    return this.alunoService.findOne(Number(mat));
  }

  @Patch(':mat')
  update(@Param('mat') mat: string, @Body() data: any) {
    return this.alunoService.update(Number(mat), data);
  }

  @Delete(':mat')
  remove(@Param('mat') mat: string) {
    return this.alunoService.remove(Number(mat));
  }
}
