local PI =  3.14159265359;

local global_y_offset = 90;
local global_x_offset = 115;

local numbers_step = 80;
local numbers_second_set_offset = 225;

local mini_numbers_y_offset = 15;
local mini_numbers_x_offset = 557;
local mini_numbers_step = 75;

local letter_y_offset = 20;
local letter_x_offset = 190;

local noise_y_bounds_deviation = 50;
local noise_x_bounds_deviation = 50;

{
  "generator_config": {
    "num_out_img": 48000, // adding more background files might be necessary
     // the more background pictures you load simultaneously, the faster the generator will be
     // this limit depends on machine's available memory.
    "background_load_limit": 100, // performance tip: background_load_limit should devide number of background images
    "apply_misc_noise": true,
    "apply_dirt": true,
    "output_directory": "output",
    "img_per_package": 6000
  },
  "annotations_config": {
    // "bg": 0,
    // all characters after '_' in the file name will be ignored
    // 'key': [address in an annotation picture, single instance]
    "plate": [8, true],
    // numbers
    "0": [16, false],
    "1": [24, false],
    "2": [32, false],
    "3": [40, false],
    "4": [48, false],
    "5": [56, false],
    "6": [64, false],
    "7": [72, false],
    "8": [80, false],
    "9": [88, false],
    // letters
    "A": [95, true],
    "B": [96, true],
    "P": [97, true],
    "T": [98, true],
    "S": [100, true],
    "J": [104, true],
    "CH": [112, true],
    "HE": [120, true],
    "KH": [128, true],
    "D": [136, true],
    "Z": [144, true],
    "R": [152, true],
    "ZE": [160, true],
    "ZH": [168, true],
    "SIN": [176, true],
    "SHIN": [184, true],
    "SAD":[192, true],
    "ZAD": [193, true],
    "TA": [194, true],
    "ZA": [195, true],
    "AIN": [196, true],
    "GHAIN": [197, true],
    "F": [198, true],
    "Q": [200, true],
    "K": [201, true],
    "G": [202, true],
    "L": [203, true],
    "M": [204, true],
    "N": [205, true],
    "V": [206, true],
    "H": [207, true],
    "Y": [208, true]
  },
  "plate_config": {
    "letter_offset": [
      global_y_offset,
      global_x_offset + letter_x_offset
    ],
    "mini_numbers_offset": [
    [
      global_y_offset + mini_numbers_y_offset,
      global_x_offset + mini_numbers_x_offset
    ],
    [
      global_y_offset + mini_numbers_y_offset,
      global_x_offset + mini_numbers_x_offset + mini_numbers_step
    ]
    ],
    "numbers_offset": [
      [
        global_y_offset,
        global_x_offset
      ],
      [
        global_y_offset,
        global_x_offset + numbers_step
      ],
      [
        global_y_offset,
        global_x_offset + numbers_step + numbers_second_set_offset
      ],
      [
        global_y_offset,
        global_x_offset + 2 * numbers_step + numbers_second_set_offset
      ],
      [
        global_y_offset,
        global_x_offset + 3 * numbers_step + numbers_second_set_offset
      ]
    ]
  },
  "noise_config":{
    "misc_probability": 0.75,
    "dirt_probability": 0.5,
    "misc_bounds": [
      {
        "y_min": 100 - noise_y_bounds_deviation,
        "y_max": 100 + noise_y_bounds_deviation,
        "x_min": 88 - noise_x_bounds_deviation,
        "x_max": 88 + noise_x_bounds_deviation
      },
      {
        "y_min": 400 - 2.5 * noise_y_bounds_deviation,
        "y_max": 400 + 2.5 * noise_y_bounds_deviation,
        "x_min": 88 - noise_x_bounds_deviation,
        "x_max": 88 + noise_x_bounds_deviation
      },
      {
        "y_min": 700 - noise_y_bounds_deviation,
        "y_max": 700 + noise_y_bounds_deviation,
        "x_min": 88 - noise_x_bounds_deviation,
        "x_max": 88 + noise_x_bounds_deviation
      }
    ]
  },
  "transformations_config": {
    "output_size": [1024,1024],
    "max_dalpha": PI / 10,
    "max_dbeta": PI / 10,
    "max_dgamma": PI / 10,
    "max_dz": 3.5 // min_dz = 1
  },
  "components": {
    "dirt": "components/dirt/*.png",
    "letters": "components/letters/*.png",
    "mini_numbers": "components/mini_numbers/*.png",
    "misc": "components/misc/*.png",
    "numbers": "components/numbers/*.png",
    "plates": "components/plates/*.png",
    "backgrounds": "components/backgrounds/*.png"
  }
}