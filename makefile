### micropython development system v1.2.3

cdc = /dev/cu.usbmodem141101
bsp_objects = $(shell find bsp -depth 1 -name "*.py" \! -name ".*")
res_objects = $(shell find res -depth 1 -name "*.py" \! -name ".*")
m ?= no_this_module.py

## show help
help :
	@echo "make help - show help"
	@echo "make repl - enter into repl mode"
	@echo "make run m=app/<filename> - run the module at once"
	@echo "make main m=app/<filename> - cp the module as main.py to board"
	@echo "make bsp - cp board support package to board"
	@echo "make res - cp resouce files to board"

## repl
repl :
	rshell -p $(cdc) repl

## run on board
run : $(m)
	pyboard --follow --device $(cdc) $(m)
#	ampy -p $(cdc) run $(m)

## flash bsp to board
bsp : reset out $(bsp_objects:bsp/%=out/%)
	@echo "bsp updated."

## flash selected module as main.py
main : bsp
	if [[ -e $(m) ]]; then rshell -p $(cdc) cp $(m) /pyboard/main.py; echo; fi
	@echo "main updated."

## flash res to board
res : reset out $(res_objects:res/%=out/%)
	@echo "res updated."

out :
	mkdir -p out

## out cache maintaining
out/%.py : bsp/%.py
	cp $< $@
	rshell -p $(cdc) cp $@ /pyboard; echo;

out/%.py : res/%.py
	cp $< $@
	rshell -p $(cdc) cp $@ /pyboard; echo;

## others
.PHONY : reset
reset :
	ampy -p $(cdc) reset

clean :
	rm -r out || true
	rshell -p $(cdc) rm -rf /pyboard
