# leaplog
A simple Leap Motion logger

## Usage
1. [Download](https://developer.leapmotion.com/sdk/v2) the __Leap Motion__ client software __v2.3.1__ for your operating system and install it.

2. Install __leaplog__ dependencies :
    ```bash
    pip2 install --user -r requirements.txt
    ```
3. Create the sqlite3 database :
    ```bash
    sqlite3 data.db < leaplog/tracking/data/sql/schema.sql
    ```
4. Start the application :
    ```bash
    python2 -m leaplog
    ```
5. The application now listens on 0.0.0.0:8000

## License
The project is MIT licensed as described in the `LICENSE` file. __Leap Motion__ documentation and libraries (`lib/` and `doc/` folders) are properties of _Ultraleap Ltd_ and are, therefore, licensed under their own terms.
