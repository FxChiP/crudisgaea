# crudisgaea

A small Flask PoC I used to teach myself a bit about Flask
and Werkzeug. As well as try to "genericize" making a CRUD
API using dataclasses.

Since it's a PoC it should be noted that any changes made
via the API will not be persisted in any way. The main proofs
are genericizing making a CRUD using dataclasses and a
class-agnostic (... mostly) object store, as well as generally
learning how to write Flask apps.

## Running it

`flask --app crudisgaea.app run`

If you want to test the auth middleware:

`API_AUTH_KEY="your_api_key_make_it_good" flask --app crudisgaea.app run`

## API

### characters 

#### /v1/characters

##### GET

A list of characters in the following format.

```json
{
    "items": [
        {
            "id": "CharacterName",
            "DisgaeaCharacter": {
                "name": "CharacterName",
                "equipment": ["sword", "armor", "emblem"]
            }
        }
    ]
}
```

##### POST

Just POST the character object like so:

```json
{
    "name": "CharacterName",
    "equipment": [
            "sword",
            "spear",
            "axe",
            "bow_arrow",
            "gun",
            "fist",
            "staff",
            "monster_phy",
            "monster_int",
            "armor",
            "belt",
            "shoes",
            "glasses",
            "orb",
            "muscle",
            "emblem",
            "special"
    ]
}
```

The `equipment` field is essentially an enum; all possible values
are given in the example above.

#### /v1/character/<char_name>

##### GET

Returns just the data of the DisgaeaCharacter object.

```json
{
    "name": "CharacterName",
    "equipment": [
            "sword",
            "spear",
            "axe",
            "bow_arrow",
            "gun",
            "fist",
            "staff",
            "monster_phy",
            "monster_int",
            "armor",
            "belt",
            "shoes",
            "glasses",
            "orb",
            "muscle",
            "emblem",
            "special"
    ]
}
```

##### POST

The same format as for /v1/characters and the GET for
a single character:

```json
{
    "name": "CharacterName",
    "equipment": [
            "sword",
            "spear",
            "axe",
            "bow_arrow",
            "gun",
            "fist",
            "staff",
            "monster_phy",
            "monster_int",
            "armor",
            "belt",
            "shoes",
            "glasses",
            "orb",
            "muscle",
            "emblem",
            "special"
    ]
}
```
