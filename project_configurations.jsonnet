local global_y_offset = 90;
local global_x_offset = 115;

local numbers_step = 80;
local numbers_second_set_offset = 225;

local mini_numbers_y_offset = 15;
local mini_numbers_x_offset = 557;
local mini_numbers_step = 75;

local letter_y_offset = 20;
local letter_x_offset = 190;

local noise_y_bounds_deviation = 40;
local noise_x_bounds_deviation = 80;

{
  "annotations_config": {
    // "bg": 0,
    // plates
    "simple": 8,
    "taxi": 8,
    // numbers
    "0": 16,
    "1": 24,
    "2": 32,
    "3": 40,
    "4": 48,
    "5": 56,
    "6": 64,
    "7": 72,
    "8": 80,
    "9": 88,
    // mini_numbers
    "0_mini": 16,
    "1_mini": 24,
    "2_mini": 32,
    "3_mini": 40,
    "4_mini": 48,
    "5_mini": 56,
    "6_mini": 64,
    "7_mini": 72,
    "8_mini": 80,
    "9_mini": 88,
    // letters
    "B": 96,
    "Dal": 104,
    "Ghaf": 112,
    "Gim": 120,
    "H": 128,
    "Lam": 136,
    "Mim": 144,
    "Nun": 152,
    "Sad": 160,
    "Sin": 168,
    "T": 176,
    "Tah": 184,
    "Vav":192,
    "Ye": 200
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
        "y_min": 400 - noise_y_bounds_deviation,
        "y_max": 400 + noise_y_bounds_deviation,
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
  },
  "components": {
    "dirt": "components/dirt/*.png",
    "letters": "components/letters/*.png",
    "mini_numbers": "components/mini_numbers/*.png",
    "misc": "components/misc/*.png",
    "numbers": "components/numbers/*.png",
    "plates": "components/plates/*.png",
  }
}