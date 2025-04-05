IDIR=./include
CFLAGS=-I$(IDIR)
LIBS=`pkg-config --cflags --libs libusbp-1`

SRCDIR=./src
ODIR=./obj

_OBJ=actuator.o tic_baud_rate.o tic_current_limit.o tic_device.o tic_error.o tic_get_settings.o tic_handle.o tic_names.o tic_set_settings.o tic_settings_fix.o tic_settings_read_from_string.o tic_settings_to_string.o tic_settings.o tic_string.o tic_variables.o yaml.o 
OBJ=$(patsubst %,$(ODIR)/%,$(_OBJ))

_OBJ2=actuator2.o tic_baud_rate.o tic_current_limit.o tic_device.o tic_error.o tic_get_settings.o tic_handle.o tic_names.o tic_set_settings.o tic_settings_fix.o tic_settings_read_from_string.o tic_settings_to_string.o tic_settings.o tic_string.o tic_variables.o yaml.o 
OBJ2=$(patsubst %,$(ODIR)/%,$(_OBJ2))

all: actuator actuator2 actuator_run

debug: CFLAGS += -g
debug: actuator actuator2

$(ODIR)/%.o: $(SRCDIR)/%.c
	$(CC) -c -o $@ $< $(CFLAGS) $(LIBS)

actuator: $(OBJ)
	gcc -o $@ $^ $(CFLAGS) $(LIBS)

actuator2: $(OBJ2)
	gcc -o $@ $^ $(CFLAGS) $(LIBS)

actuator_run:
	gcc -o actuator_run actuator_run.c

clean:
	del.bat &> null
# gcc -o actuator actuator.c tic_baud_rate.c tic_current_limit.c tic_device.c tic_error.c tic_get_settings.c tic_handle.c tic_names.c tic_set_settings.c tic_settings_fix.c tic_settings_read_from_string.c tic_settings_to_string.c tic_settings.c tic_string.c tic_variables.c yaml.c -I./../include `pkg-config --cflags --libs libusbp-1`
