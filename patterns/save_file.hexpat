struct Monster {
    u8 name[12];
    u8 unknown_a[6];
    u16 species_id;
    u8 unknown_b[10];
    u16 age;
    u8 unknown_c[8];
    u16 power;
    u16 intelligence;
    u16 skill;
    u16 speed;
    u16 defense;
    u16 life;
    u8 unknown_d[368];
};

struct SaveEntry {
    u8 save_counter;
    u8 unknown_a[4];
    bool did_not_quit;
    u8 unknown_b[4];
    u8 ranch_name[13];
    u8 unknown_c[4];
    u8 player_name[13];
    u8 unknown_d[16];
    u32 header_checksum;
    u8 unknown_e[10];
    u8 breeder_grade;
    u8 unknown_f[69];
    u32 money_won;
    u8 unknown_g[80];
    u8 monster_breed_max_grades[29];
    u8 unknown_h[99];
    u32 gold;
    u16 items[50];
    Monster monsters[31];
    u8 unknown_i[2104];
    u32 checksum;
};

struct SaveFile {
    u8 header[34];
    SaveEntry entries[2];
};

SaveFile save @ 0x0;