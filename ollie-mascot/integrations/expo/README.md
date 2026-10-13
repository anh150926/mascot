# Ollie trong ứng dụng Expo

Thư mục này là bộ có thể sao chép vào ứng dụng Expo: component TypeScript, `ollie.riv`, ảnh dự phòng và hợp đồng `mood`. File Rive được đóng gói cục bộ, nên hoạt động khi không có mạng. `OllieContract.ts` và `assets/` được cập nhật từ bản build bằng `python tools/package_expo.py`.

## Yêu cầu

Rive React Native mới (`@rive-app/react-native`) cần Expo SDK 53+, React Native 0.78+, iOS 15.1+ hoặc Android SDK 24+. Nó dùng Nitro Modules, vì vậy hãy chạy **Expo development build** hoặc bản release của app; Expo Go không chứa module native này. Đối chiếu phiên bản trong `package.json` của app với [tài liệu Rive React Native](https://rive.app/docs/runtimes/react-native/react-native) trước khi nâng cấp.

Component này đã được kiểm tra kiểu với `@rive-app/react-native` 0.5.4, `react-native-nitro-modules` 0.35.10 và React Native 0.79.7. Bản native của app cần được build và thử trên thiết bị riêng.

## Cài vào app

1. Sao chép cả thư mục `integrations/expo` vào app, ví dụ `src/ollie/`.
2. Cài runtime trong thư mục app:

   ```sh
   npx expo install @rive-app/react-native react-native-nitro-modules
   ```

3. Trong `metro.config.js` của app, thêm `riv` vào `assetExts` hiện có:

   ```js
   const { getDefaultConfig } = require("expo/metro-config");

   const config = getDefaultConfig(__dirname);
   if (!config.resolver.assetExts.includes("riv")) {
     config.resolver.assetExts.push("riv");
   }

   module.exports = config;
   ```

   Nếu app đã có cấu hình Metro, chỉ thêm phần mở rộng vào cấu hình đó. Rive [khuyến nghị nạp file bằng `require()`](https://rive.app/docs/runtimes/react-native/loading-rive-files) để Expo đóng gói asset vào release và hỗ trợ cập nhật OTA.

4. Tạo development build (`npx expo run:android` hoặc `npx expo run:ios` trên macOS), rồi chạy ứng dụng. Khi thêm hoặc cập nhật native package, cần build lại binary.

## Sử dụng

```tsx
import { useState } from "react";
import { Button, View } from "react-native";
import { OllieMascot } from "./ollie/OllieMascot";
import type { OllieMood } from "./ollie/OllieContract";

export function OllieExample() {
  const [mood, setMood] = useState<OllieMood>("neutral");
  const [asleep, setAsleep] = useState(false);
  const [waveToken, setWaveToken] = useState(0);

  return (
    <View>
      <OllieMascot
        mood={mood}
        asleep={asleep}
        onAsleepChange={setAsleep}
        waveToken={waveToken}
        size={240}
        active={true}
        onError={console.warn}
      />
      <Button title="Suy nghĩ" onPress={() => setMood("thinking")} />
      <Button title="Vẫy cánh" onPress={() => setWaveToken((n) => n + 1)} />
      <Button title="Ngủ / thức" onPress={() => setAsleep((value) => !value)} />
    </View>
  );
}
```

Đặt `active={false}` khi màn hình chứa Ollie không còn hiển thị để tạm dừng vẽ. `frameRate` mặc định 30 FPS và có thể tăng lên 60 nếu cần. Đặt lời thoại bằng một View/Text của app bên ngoài Rive; file `.riv` chỉ chứa hình và chuyển động. `onAsleepChange` giúp state của app theo kịp khi người dùng chạm Ollie để đánh thức.

## Đồng bộ trước release

Từ thư mục `ollie-mascot`:

```sh
python tools/build_kit.py
python tools/package_expo.py --check
```

Build đầy đủ tự cập nhật gói Expo sau khi xuất `.riv`. `--check` so sánh asset và hợp đồng với bản dựng hiện hành. Hãy thử `neutral`, `thinking`, `sleep/wake`, `wave` và một cảnh trong thư viện trên cả Android lẫn iOS bằng **release build** trước khi phát hành.
