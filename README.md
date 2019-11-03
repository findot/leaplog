# leaplog
A simple Leap Motion logger

## Usage
1. Install __leaplog__ dependencies :
    ```bash
    pip2 install --user -r requirements.txt
    ```
2. Create the sqlite3 database :
    ```bash
    sqlite3 data.db < leaplog/tracking/data/sql/schema.sql
    ```
3. Start the application :
    ```bash
    python2 -m leaplog
    ```
4. The application now listens on 0.0.0.0:8000

## License
The project is MIT licensed as described in the `LICENSE` file. __Leap Motion__ documentation and libraries (`lib/` and `doc/` folders) are properties of _Ultraleap Ltd_ and are, therefore, licensed under their own terms.
