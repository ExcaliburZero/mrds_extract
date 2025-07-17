// Make sure to set base address to 0x2000000

struct Monster {
    u8 name[12];
    u8 unknown_a[6] [[color("000000")]];
    u16 species_id;
    u8 unknown_b[10] [[color("000000")]];
    u16 age;
    u16 remaining_lifespan;
    u8 unknown_c[6] [[color("000000")]];
    u16 power;
    u16 intelligence;
    u16 skill;
    u16 speed;
    u16 defense;
    u16 life;
    u8 unknown_d[368] [[color("000000")]];
};

struct SaveEntry {
    u8 save_counter;
    u8 unknown_a[4] [[color("000000")]];
    u8 unknown_maybe_related_to_quitting_without_saving;
    u8 unknown_b[4] [[color("000000")]];
    u8 ranch_name[13];
    u8 unknown_c[4] [[color("000000")]];
    u8 player_name[13];
    u8 unknown_d[8] [[color("000000")]];
    u16 year;
    u8 month;
    u8 week;
    u8 day_of_week;
    u8 unknown_e[3] [[color("000000")]];
    u32 header_checksum;
    u8 unknown_f[10] [[color("000000")]];
    u8 breeder_grade;
    u8 unknown_g[69] [[color("000000")]];
    u32 money_won;
    u8 unknown_h[80] [[color("000000")]];
    u8 monster_breed_max_grades[29];
    u8 unknown_i[63] [[color("000000")]];
    u8 encyclopedia_unlocked_monsters[34];
    u8 unknown_j[2] [[color("000000")]];
    u32 gold;
    u16 items[50];
    Monster monsters[31];
    u8 unknown_k[2104] [[color("000000")]];
    u32 checksum;
};

SaveEntry save_entry @ 0x21B6530;