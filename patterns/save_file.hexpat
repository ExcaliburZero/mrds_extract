struct Monster {
    u8 name[12];
    u8 unknown_a[6];
    u16 species_id;
    u8 unknown_b[20];
    u16 power;
    u16 intelligence;
    u16 skill;
    u16 speed;
    u16 defense;
    u16 life;
    u8 unknown_c[368];
};

struct SaveEntry {
    u8 unknown_a[10];
    u8 ranch_name[13];
    u8 unknown_b[4];
    u8 player_name[13];
    u8 unknown_c[16];
    u32 header_checksum;
    u8 unknown_d[292];
    u32 gold;
    u16 items[50];
    Monster monsters[31];
    u8 unknown_f[2104];
    u32 checksum;
};

struct SaveFile {
    u8 header[34];
    SaveEntry entries[2];
};

SaveFile save @ 0x0;