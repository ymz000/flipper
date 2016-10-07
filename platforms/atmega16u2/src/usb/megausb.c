#define __private_include__
#include <private/megausb.h>
#include <platform/atmega16u2.h>

const struct _lf_endpoint megausb = {
	megausb_configure,
	megausb_ready,
	megausb_put,
	megausb_get,
	megausb_push,
	megausb_pull,
	megausb_destroy
};

int megausb_configure(struct _lf_endpoint *endpoint) {
	return lf_success;
}

uint8_t megausb_ready(void) {
	return 0;
}

void megausb_put(uint8_t byte) {

}

uint8_t megausb_get(void) {
	return 0;
}

int megausb_push(void *source, lf_size_t length) {
	int8_t bytes = megausb_bulk_transmit(source, length);
	if (bytes <= 0) {
		return lf_error;
	}
	return lf_success;
}

int megausb_pull(void *destination, lf_size_t length) {
	int8_t bytes = megausb_bulk_receive(destination, length);
	if (bytes <= 0) {
		return lf_error;
	}
	return 	lf_success;
}

int megausb_destroy(struct _lf_endpoint *endpoint) {
	return lf_success;
}
