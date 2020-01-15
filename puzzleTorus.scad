$fn=256;

difference() {
	union() {
		difference() {
			rotate_extrude(convexity = 10) {
				translate(v = [30.0000000000, 0]) {
					intersection() {
						circle(r = 14.0000000000);
						square(center = true, size = [225.0000000000, 23.980762113533157]);
					}
				}
			}
			translate(v = [-30.0000000000, 0, 15.0000000000]) {
				cube(center = true, size = [60.0000000000, 27.980762113533157, 30.0000000000]);
			}
		}
		intersection() {
			intersection() {
				rotate(a = [45, 0, 0]) {
					cube(center = true, size = [120.0000000000, 15.0000000000, 15.0000000000]);
				}
			}
			rotate_extrude(convexity = 10) {
				translate(v = [30.0000000000, 0]) {
					intersection() {
						circle(r = 14.0000000000);
						square(center = true, size = [225.0000000000, 23.980762113533157]);
					}
				}
			}
		}
	}
	union() {
		translate(v = [30.0000000000, -6.495190528383289, 0]) {
			cube(center = true, size = [60.0000000000, 14.990381056766578, 30.0000000000]);
		}
		translate(v = [60.0000000000, 0, 0]) {
			intersection() {
				rotate(a = [45, 0, 0]) {
					cube(center = true, size = [120.0000000000, 15.0000000000, 15.0000000000]);
				}
			}
		}
	}
}
