; ModuleID = "brainfuck"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define void @"main"()
{
entry:
  %".2" = call i8* @"calloc"(i32 65536, i32 1)
  store i8* %".2", i8** @"array"
  call void @"inc"()
  call void @"inc"()
  call void @"mov_right"()
  call void @"inc"()
  call void @"inc"()
  call void @"inc"()
  call void @"inc"()
  call void @"inc"()
  %".12" = load i32, i32* @"index"
  %".13" = icmp ne i32 %".12", 0
  br i1 %".13", label %"body_0", label %"end_0"
body_0:
  call void @"mov_left"()
  call void @"inc"()
  call void @"mov_right"()
  call void @"dec"()
  %".19" = load i32, i32* @"index"
  %".20" = icmp ne i32 %".19", 0
  br i1 %".20", label %"body_0", label %"end_0"
end_0:
  call void @"inc"()
  call void @"inc"()
  call void @"inc"()
  call void @"inc"()
  call void @"inc"()
  call void @"inc"()
  call void @"inc"()
  call void @"inc"()
  %".30" = load i32, i32* @"index"
  %".31" = icmp ne i32 %".30", 0
  br i1 %".31", label %"body_1", label %"end_1"
body_1:
  call void @"mov_left"()
  call void @"inc"()
  call void @"inc"()
  call void @"inc"()
  call void @"inc"()
  call void @"inc"()
  call void @"inc"()
  call void @"mov_right"()
  call void @"dec"()
  %".42" = load i32, i32* @"index"
  %".43" = icmp ne i32 %".42", 0
  br i1 %".43", label %"body_1", label %"end_1"
end_1:
  call void @"mov_left"()
  call void @"output"()
  call void @"free"(i8* %".2")
  ret void
}

@"index" = global i32 0
@"array" = global i8* null
declare i32 @"getchar"()

declare i32 @"putchar"(i32 %".1")

declare i8* @"calloc"(i32 %".1", i32 %".2")

declare void @"free"(i8* %".1")

define void @"inc"()
{
entry:
  %".2" = load i8*, i8** @"array"
  %".3" = load i32, i32* @"index"
  %".4" = getelementptr i8, i8* %".2", i32 %".3"
  %".5" = load i8, i8* %".4"
  %".6" = add i8 %".5", 1
  store i8 %".6", i8* %".4"
  ret void
}

define void @"dec"()
{
entry:
  %".2" = load i8*, i8** @"array"
  %".3" = load i32, i32* @"index"
  %".4" = getelementptr i8, i8* %".2", i32 %".3"
  %".5" = load i8, i8* %".4"
  %".6" = sub i8 %".5", 1
  store i8 %".6", i8* %".4"
  ret void
}

define void @"input"()
{
entry:
  %".2" = load i8*, i8** @"array"
  %".3" = load i32, i32* @"index"
  %".4" = getelementptr i8, i8* %".2", i32 %".3"
  %".5" = call i32 @"getchar"()
  %".6" = trunc i32 %".5" to i8
  store i8 %".6", i8* %".4"
  ret void
}

define void @"output"()
{
entry:
  %".2" = load i8*, i8** @"array"
  %".3" = load i32, i32* @"index"
  %".4" = getelementptr i8, i8* %".2", i32 %".3"
  %".5" = load i8, i8* %".4"
  %".6" = zext i8 %".5" to i32
  %".7" = call i32 @"putchar"(i32 %".6")
  ret void
}

define void @"mov_left"()
{
entry:
  %".2" = load i32, i32* @"index"
  %".3" = sub i32 %".2", 1
  store i32 %".3", i32* @"index"
  ret void
}

define void @"mov_right"()
{
entry:
  %".2" = load i32, i32* @"index"
  %".3" = add i32 %".2", 1
  store i32 %".3", i32* @"index"
  ret void
}
