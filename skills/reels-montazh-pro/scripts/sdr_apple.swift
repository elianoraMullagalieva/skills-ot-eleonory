// HDR (Dolby Vision / HLG с iPhone) → SDR Rec.709 силами Apple — тот же движок, что у «Фото» при экспорте.
// Разрешение, fps и звук сохраняются. Только macOS.
//   swift sdr_apple.swift вход.MOV выход.mov [hevc|h264]
// hevc (по умолчанию) — HEVC SDR максимального качества (битность как у исходника); h264 — H.264 8 бит.
// Свой LUT/тонмаппинг НЕ делаем: у Apple результат лучше (проверено — самодельный LUT даёт «ужасную цветокоррекцию»).
import AVFoundation

let a = CommandLine.arguments
guard a.count >= 3 else {
  print("использование: swift sdr_apple.swift вход.MOV выход.mov [hevc|h264]"); exit(2)
}
let src = URL(fileURLWithPath: a[1]), dst = URL(fileURLWithPath: a[2])
let preset = (a.count > 3 && a[3] == "h264") ? AVAssetExportPresetHighestQuality : AVAssetExportPresetHEVCHighestQuality
try? FileManager.default.removeItem(at: dst)
let asset = AVURLAsset(url: src)
let sem = DispatchSemaphore(value: 0)
var code: Int32 = 0
Task {
  do {
    let vc = try await AVMutableVideoComposition.videoComposition(withPropertiesOf: asset)
    vc.colorPrimaries = AVVideoColorPrimaries_ITU_R_709_2
    vc.colorTransferFunction = AVVideoTransferFunction_ITU_R_709_2
    vc.colorYCbCrMatrix = AVVideoYCbCrMatrix_ITU_R_709_2
    guard let ex = AVAssetExportSession(asset: asset, presetName: preset) else {
      print("не удалось создать сессию экспорта"); code = 1; sem.signal(); return
    }
    ex.outputURL = dst; ex.outputFileType = .mov; ex.videoComposition = vc
    let timer = DispatchSource.makeTimerSource(queue: .global())
    timer.schedule(deadline: .now() + 5, repeating: 5)
    timer.setEventHandler { print(String(format: "  %.0f%%", ex.progress * 100)) }
    timer.resume()
    await ex.export()
    timer.cancel()
    if ex.status == .completed { print("ok", dst.path) } else {
      print("ошибка:", ex.error?.localizedDescription ?? "status \(ex.status.rawValue)"); code = 1
    }
  } catch { print("ошибка:", error); code = 1 }
  sem.signal()
}
sem.wait()
exit(code)
