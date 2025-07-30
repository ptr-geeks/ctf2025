#include <stdio.h>

struct Interpreter {
	char tape[256];
	char program[256];
	int backtrace[64];
	int tape_ptr;
	int prog_ptr;
	int backtrace_ptr;
} interpreter = {
	.tape = {0},
	.program = {0},
	.backtrace = {0},
	.tape_ptr = 0,
	.prog_ptr = 0,
	.backtrace_ptr = 0
};

void cmd_inc() { // +
	interpreter.tape[interpreter.tape_ptr]++;
}

void cmd_dec() { // -
	interpreter.tape[interpreter.tape_ptr]--;
}

void cmd_right() { // >
	interpreter.tape_ptr++;
}

void cmd_left() { // <
	interpreter.tape_ptr--;
}

void cmd_output() { // .
	putchar(interpreter.tape[interpreter.tape_ptr]);
}

void cmd_input() { // ,
	interpreter.tape[interpreter.tape_ptr] = getchar();
}

void cmd_loop_start() { // [
	if (interpreter.tape[interpreter.tape_ptr] != 0) {
		interpreter.backtrace[interpreter.backtrace_ptr++] = interpreter.prog_ptr;
		return;
	}

	while (1) {
		interpreter.prog_ptr++;
		if (interpreter.program[interpreter.prog_ptr] == ']')
			break;
		if (interpreter.program[interpreter.prog_ptr] == '\0') {
			interpreter.prog_ptr--;
			break;
		}
	}
}

void cmd_loop_end() { // ]
	if (interpreter.tape[interpreter.tape_ptr] != 0) {
		interpreter.prog_ptr = interpreter.backtrace[interpreter.backtrace_ptr - 1];
		return;
	}

	interpreter.backtrace_ptr--;
}

void run() {
	while (interpreter.program[interpreter.prog_ptr] != '\0') {
		switch (interpreter.program[interpreter.prog_ptr]) {
			case '+': cmd_inc(); break;
			case '-': cmd_dec(); break;
			case '>': cmd_right(); break;
			case '<': cmd_left(); break;
			case '.': cmd_output(); break;
			case ',': cmd_input(); break;
			case '[': cmd_loop_start(); break;
			case ']': cmd_loop_end(); break;
			default: break;
		}

		interpreter.prog_ptr++;
	}
}

int main() {
	setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);

	puts("Program: ");
	fgets(interpreter.program, sizeof(interpreter.program), stdin);

	puts("Initial tape: ");
	fgets(interpreter.tape, sizeof(interpreter.tape), stdin);

	puts("Running");
	run();

	puts(interpreter.tape);
	return 0;
}  
