{-|
Module      : Flipper.Internal.FMR
Description : Internal FMR Module
Copyright   : George Morgan, Travis Whitaker 2016
License     : All rights reserved.
Maintainer  : travis@flipper.io
Stability   : Provisional
Portability : Windows, POSIX

-}

module Flipper.Internal.FMR (
    FMRModule()
  , bind
  , invoke
  ) where

import Data.Word

import Foreign.C.String
import Foreign.Ptr
import Foreign.Storable
import Foreign.Marshal.Alloc

-- | FMR module identifier.
newtype FMRModule = FMRModule { unFMRModule :: Word32 }

bind :: String -> IO FMRModule
bind s = withCString s ((FMRModule <$>) . c_fmr_bind)

fmrCellSize :: Int
fmrCellSize = (sizeOf (undefined :: Word32)) + (sizeOf (undefined :: Ptr Word8))

fmrList :: [Word32] -> (Ptr Word8 -> IO a) -> IO a
fmrList [] f = f nullPtr
fmrList as f = allocaBytes fmrCellSize (\p -> go p p as)
    where go p c (a:[]) = do
                poke (castPtr c) a
                poke (plusPtr (castPtr c) (sizeOf a)) nullPtr
                f p
          go p c (a:as) = allocaBytes fmrCellSize $ \c' -> do
                poke (castPtr c) a
                poke (plusPtr (castPtr c) (sizeOf a)) c'
                go p c' as

invoke :: FMRModule -> Word8 -> [Word32] -> IO Word32
invoke (FMRModule m) i as = fmrList as (c_fmr_invoke_list m i)

foreign import ccall safe "flipper/fmr.h fmr_bind"
    c_fmr_bind :: CString -> IO Word32

foreign import ccall safe "flipper/fmr.h fmr_invoke_list"
    c_fmr_invoke_list :: Word32 -> Word8 -> Ptr Word8 -> IO Word32

-- "fmr_resolve" not yet implemented...