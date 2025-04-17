# main.py (머신 내부)
from saucemill_firmware import main
import uasyncio

print("👟 main.mpy 내 main() 실행 시작")
uasyncio.run(main())
