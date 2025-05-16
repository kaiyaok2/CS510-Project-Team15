/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.commons.fileupload.util.mime;

import java.io.IOException;
import java.io.OutputStream;

/**
 * @since 1.3
 */
final class QuotedPrintableDecoder {

    /**
     * The shift value required to create the upper nibble from the first of 2 byte values converted
     * from ascii hex.
     */
    private static final int UPPER_NIBBLE_SHIFT = Byte.SIZE / 2;

    /** Hidden constructor, this class must not be instantiated. */
    private QuotedPrintableDecoder() {}

    /**
     * Decode the encoded byte data writing it to the given output stream.
     *
     * @param data The array of byte data to decode.
     * @param out The output stream used to return the decoded data.
     * @return the number of bytes produced.
     * @throws IOException
     */
    public static int decode(byte[] data, OutputStream out) throws IOException {
        int off = 0;
        int length = data.length;
        int endOffset = off + length;
        int bytesWritten = 0;

        while (off < endOffset) {
            byte ch = data[off++];

            if (ch == '_') {
                out.write(' ');
            } else if (ch == '=') {
                if (off + 1 >= endOffset) {
                    throw new IOException(
                            "Invalid quoted printable encoding; truncated escape sequence");
                }

                byte b1 = data[off++];
                byte b2 = data[off++];

                if (b1 == '\r') {
                    if (b2 != '\n') {
                        throw new IOException(
                                "Invalid quoted printable encoding; CR must be followed by LF");
                    }
                } else {
                    int c1 = hexToBinary(b1);
                    int c2 = hexToBinary(b2);
                    out.write((c1 << UPPER_NIBBLE_SHIFT) | c2);
                    bytesWritten++;
                }
            } else {
                out.write(ch);
                bytesWritten++;
            }
        }

        return bytesWritten;
    }

    /**
     * Convert a hex digit to the binary value it represents.
     *
     * @param b the ascii hex byte to convert (0-0, A-F, a-f)
     * @return the int value of the hex byte, 0-15
     * @throws IOException if the byte is not a valid hex digit.
     */
    private static int hexToBinary(final byte b) throws IOException {
        final int i = Character.digit((char) b, 16);
        if (i == -1) {
            throw new IOException("Invalid quoted printable encoding: not a valid hex digit: " + b);
        }
        return i;
    }
}
