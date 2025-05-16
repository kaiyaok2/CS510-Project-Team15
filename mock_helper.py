import builtins
import importlib
import pkgutil
import os
import sys
import inspect
import re
import urllib
import ast
from datetime import datetime, timedelta, timezone
from io import BytesIO, StringIO, BufferedReader, TextIOWrapper, BufferedWriter
from pathlib import Path
from urllib.parse import urlparse
from collections.abc import Iterator
from enum import Enum
from threading import Thread

reference_dict = {}

def clear_reference_dict():
    global reference_dict
    reference_dict.clear()

def import_all_modules_from_folder(folder_path):
    """
    Dynamically imports all modules from a given folder.
    
    Args:
        folder_path (str): Absolute path to the folder containing modules/packages.
    """

    folder_path = os.path.abspath(folder_path)
    parent_folder = os.path.dirname(folder_path)
    
    if parent_folder not in sys.path:
        sys.path.insert(0, parent_folder)

    package_name = os.path.basename(folder_path)

    for _, module_name, _ in pkgutil.walk_packages([folder_path], f"{package_name}."):
        full_module_name = f"{module_name}"
        try:
            module = importlib.import_module(full_module_name)
            
            for name, obj in inspect.getmembers(module):
                if isinstance(obj, type):
                    globals()[f"{module_name}.{name}"] = obj
        except Exception as e:
            continue


import_all_modules_from_folder("src")

class PeekableIterator:
    def __init__(self, iterable):
        self.iterable = iterable
        self.iterator = iter(iterable)
        self.peeked = None
        self.history = []
        self.index = -1

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= 0:
            value = self.history[self.index]
            self.index -= 1
            return value

        if self.peeked is not None:
            next_item = self.peeked
            self.peeked = None
        else:
            next_item = next(self.iterator)

        self.history.append(next_item)
        return next_item

    def hasNext(self):
        if self.peeked is None:
            try:
                self.peeked = next(self.iterator)
            except StopIteration:
                return False
        return True

    def previous(self):
        if self.hasPrevious():
            self.index += 1
            return self.history[self.index]
        raise StopIteration("No previous elements.")

    def hasPrevious(self):
        return self.index + 1 < len(self.history)

    def to_list(self):
        result = self.history[:]
        if self.peeked is not None:
            result.append(self.peeked)

        if isinstance(self.iterable, PeekableIterator):
            remaining = self.iterable.to_list()[len(self.history):]  # Get only unseen elements
        else:
            remaining = list(self.iterator)

        return result + remaining
    
class HelpFormatterTest_AnonymousClass_1:
    def __call__(self, opt1, opt2):
        opt1_key_casefold =  opt1.getKey().casefold()
        opt2_key_casefold =  opt2.getKey().casefold()
        return (opt2_key_casefold > opt1_key_casefold) - (opt2_key_casefold < opt1_key_casefold)

type_map = {
    "src.main.org.apache.commons.fileupload.disk.DiskFileItem": "src.main.org.apache.commons.fileupload.disk.DiskFileItem.DiskFileItem",
    "src.main.org.apache.commons.fileupload.FileUpload": "src.main.org.apache.commons.fileupload.FileUpload.FileUpload",
    "src.main.org.apache.commons.fileupload.MultipartStream": "src.main.org.apache.commons.fileupload.MultipartStream.MultipartStream",
    "src.main.org.apache.commons.fileupload.ProgressListener": "src.main.org.apache.commons.fileupload.ProgressListener.ProgressListener",
    "src.main.org.apache.commons.fileupload.UploadContext": "src.main.org.apache.commons.fileupload.UploadContext.UploadContext",
    "src.main.org.apache.commons.fileupload.FileItemStream": "src.main.org.apache.commons.fileupload.FileItemStream.FileItemStream",
    "src.main.org.apache.commons.fileupload.portlet.PortletFileUpload": "src.main.org.apache.commons.fileupload.portlet.PortletFileUpload.PortletFileUpload",
    "src.main.org.apache.commons.fileupload.DefaultFileItem": "src.main.org.apache.commons.fileupload.DefaultFileItem.DefaultFileItem",
    "src.main.org.apache.commons.fileupload.MultipartStream$ProgressNotifier": "src.main.org.apache.commons.fileupload.MultipartStream.ProgressNotifier",
    "src.main.org.apache.commons.fileupload.MultipartStream$ItemInputStream": "src.main.org.apache.commons.fileupload.MultipartStream.ItemInputStream",
    "src.main.org.apache.commons.fileupload.RequestContext": "src.main.org.apache.commons.fileupload.RequestContext.RequestContext",
    "src.main.org.apache.commons.fileupload.ParameterParser": "src.main.org.apache.commons.fileupload.ParameterParser.ParameterParser",
    "src.main.org.apache.commons.fileupload.util.mime.QuotedPrintableDecoder": "src.main.org.apache.commons.fileupload.util.mime.QuotedPrintableDecoder.QuotedPrintableDecoder",
    "src.main.org.apache.commons.fileupload.util.Closeable": "src.main.org.apache.commons.fileupload.util.Closeable.Closeable",
    "src.main.org.apache.commons.fileupload.util.FileItemHeadersImpl": "src.main.org.apache.commons.fileupload.util.FileItemHeadersImpl.FileItemHeadersImpl",
    "src.main.org.apache.commons.fileupload.FileItem": "src.main.org.apache.commons.fileupload.FileItem.FileItem",
    "src.main.org.apache.commons.fileupload.FileItemFactory": "src.main.org.apache.commons.fileupload.FileItemFactory.FileItemFactory",
    "src.main.org.apache.commons.fileupload.FileItemHeaders": "src.main.org.apache.commons.fileupload.FileItemHeaders.FileItemHeaders",
    "src.main.org.apache.commons.fileupload.util.Streams": "src.main.org.apache.commons.fileupload.util.Streams.Streams",
    "src.main.org.apache.commons.fileupload.disk.DiskFileItemFactory": "src.main.org.apache.commons.fileupload.disk.DiskFileItemFactory.DiskFileItemFactory",
    "src.main.org.apache.commons.fileupload.util.mime.Base64Decoder": "src.main.org.apache.commons.fileupload.util.mime.Base64Decoder.Base64Decoder",
    "src.main.org.apache.commons.fileupload.util.mime.MimeUtility": "src.main.org.apache.commons.fileupload.util.mime.MimeUtility.MimeUtility",
    "src.main.org.apache.commons.fileupload.FileUploadBase": "src.main.org.apache.commons.fileupload.FileUploadBase.FileUploadBase",
    "src.main.org.apache.commons.fileupload.util.LimitedInputStream": "src.main.org.apache.commons.fileupload.util.LimitedInputStream.LimitedInputStream",
    "src.main.org.apache.commons.fileupload.FileItemIterator": "src.main.org.apache.commons.fileupload.FileItemIterator.FileItemIterator",
    "src.main.org.apache.commons.fileupload.FileItemHeadersSupport": "src.main.org.apache.commons.fileupload.FileItemHeadersSupport.FileItemHeadersSupport",
    "src.main.org.apache.commons.fileupload.servlet.ServletRequestContext": "src.main.org.apache.commons.fileupload.servlet.ServletRequestContext.ServletRequestContext",
    "src.main.org.apache.commons.fileupload.ProgressListener": "src.main.org.apache.commons.fileupload.ProgressListener.ProgressListener",
    "src.main.org.apache.commons.fileupload.DefaultFileItemFactory": "src.main.org.apache.commons.fileupload.DefaultFileItemFactory.DefaultFileItemFactory",
    "src.main.org.apache.commons.fileupload.FileCountLimitExceededException": "src.main.org.apache.commons.fileupload.FileCountLimitExceededException.FileCountLimitExceededException",
    "src.main.org.apache.commons.fileupload.FileUploadException": "src.main.org.apache.commons.fileupload.FileUploadException.FileUploadException",
    "src.main.org.apache.commons.fileupload.FileUploadBase$FileUploadIOException": "src.main.org.apache.commons.fileupload.FileUploadBase.FileUploadIOException",
    "src.main.org.apache.commons.fileupload.FileUploadBase$FileItemIteratorImpl": "src.main.org.apache.commons.fileupload.FileUploadBase.FileItemIteratorImpl",
    "src.main.org.apache.commons.fileupload.FileUploadBase$FileItemIteratorImpl$FileItemStreamImpl": "src.main.org.apache.commons.fileupload.FileUploadBase.FileItemStreamImpl",
    "src.main.org.apache.commons.fileupload.FileUploadBase$InvalidContentTypeException": "src.main.org.apache.commons.fileupload.FileUploadBase.InvalidContentTypeException",
    "src.main.org.apache.commons.fileupload.FileUploadBase$IOFileUploadException": "src.main.org.apache.commons.fileupload.FileUploadBase.IOFileUploadException",
    "src.main.org.apache.commons.fileupload.FileUploadBase$SizeException": "src.main.org.apache.commons.fileupload.FileUploadBase.SizeException",
    "src.main.org.apache.commons.fileupload.FileUploadBase$UnknownSizeException": "src.main.org.apache.commons.fileupload.FileUploadBase.UnknownSizeException",
    "src.main.org.apache.commons.fileupload.FileUploadBase$SizeLimitExceededException": "src.main.org.apache.commons.fileupload.FileUploadBase.SizeLimitExceededException",
    "src.main.org.apache.commons.fileupload.FileUploadBase$FileSizeLimitExceededException": "src.main.org.apache.commons.fileupload.FileUploadBase.FileSizeLimitExceededException",
    "src.main.org.apache.commons.fileupload.FileItemStream$ItemSkippedException": "src.main.org.apache.commons.fileupload.FileItemStream.ItemSkippedException",
    "src.main.org.apache.commons.fileupload.InvalidFileNameException": "src.main.org.apache.commons.fileupload.InvalidFileNameException.InvalidFileNameException",
    "src.main.org.apache.commons.fileupload.MultipartStream$MalformedStreamException": "src.main.org.apache.commons.fileupload.MultipartStream.MalformedStreamException",
    "src.main.org.apache.commons.fileupload.MultipartStream$IllegalBoundaryException": "src.main.org.apache.commons.fileupload.MultipartStream.IllegalBoundaryException",
    "java.lang.Byte": "int",
    "java.lang.Boolean": "bool",
    "java.lang.Character": "str",
    "java.lang.IllegalStateException": "RuntimeError",
    "java.lang.IllegalArgumentException": "ValueError",
    "java.lang.Integer": "int",
    "java.lang.Float": "float",
    "java.lang.Object": "object",
    "java.lang.String": "str",
    "java.lang.Throwable": "Exception",
    "java.io.InputStream": "None",
    "java.io.ByteArrayInputStream": "io.BytesIO",
    "java.io.ByteArrayOutputStream": "io.BytesIO",
    "java.io.IOException": "OSError",
    "java.io.UnsupportedEncodingException": "ValueError",
    "java.util.Arrays$ArrayList": "list",
    "java.util.ArrayList": "list",
    "java.util.LinkedList": "list",
    "java.util.HashMap":"dict",
    "java.util.HashSet":"set",
    "java.util.Iterator": "PeekableIterator",
    "java.util.LinkedHashMap":"dict",
    "java.util.Map":"dict",
    "java.util.TreeMap":"dict",
    "ArrayList": "list",
    "LinkedList": "list",
    "byte": "int",
    "int": "int",
    "long": "int",
    "char": "str",
    "boolean": "bool",
    "null": "None",
    "java.lang.Long": "int",
    "Assert": "unittest.TestCase",
    "java.lang.NumberFormatException": "ValueError",
    "java.lang.UnsupportedOperationException": "RuntimeError",
    "java.lang.Float": "float",
    "java.lang.ClassNotFoundException": "ModuleNotFoundError",
    "java.util.Enumeration": "PeekableIterator",
    "java.lang.RuntimeException": "RuntimeError",
    "java.util.ListIterator": "PeekableIterator",
    "java.lang.CloneNotSupportedException": "TypeError",
    "java.util.Vector": "list",
    "java.lang.Double": "float",
    "java.util.Properties": "dict",
    "java.io.FileNotFoundException": "FileNotFoundError",
    "java.net.MalformedURLException": "ValueError",
    "java.util.Arrays": "list",
    "java.lang.Class": "type",
    "java.util.Collections$UnmodifiableRandomAccessList": "tuple",
    "java.util.Collections$SingletonList": "list",
    "java.util.Comparator": "typing.Callable",
    "java.io.PrintWriter": "io.StringIO",
    "java.lang.StringBuffer": "io.StringIO",
    "java.lang.Number": "numbers.Number",
    "java.net.URL": "urllib.parse.ParseResult",
    "java.util.Date": "datetime.datetime",
    "java.util.Calendar": "datetime.datetime",
    "java.time.Instant": "datetime.datetime",
    "java.time.Clock": "datetime.datetime",
    "java.util.concurrent.atomic.AtomicInteger": "int",
    "java.io.File": "pathlib.Path",
    "java.util.Collections$UnmodifiableCollection": "tuple",
    "java.io.FileInputStream": "io.FileIO",
    "java.io.FileOutputStream": "io.FileIO",
    "java.util.LinkedHashMap$LinkedValues": "dict_values",
    "java.util.LinkedHashMap$LinkedKeySet": "dict_keys",
    "java.lang.Short": "int",
    "java.util.Collections$EmptyList": "list",
    "src.main.org.apache.commons.cli.MissingOptionException": "src.main.org.apache.commons.cli.MissingOptionException.MissingOptionException",
    "src.main.org.apache.commons.cli.HelpFormatter$OptionComparator": "src.main.org.apache.commons.cli.HelpFormatter.OptionComparator",
    "src.main.org.apache.commons.cli.CommandLine$Builder": "src.main.org.apache.commons.cli.CommandLine.Builder",
    "src.main.org.apache.commons.cli.Option$Builder": "src.main.org.apache.commons.cli.Option.Builder",
    "src.main.org.apache.commons.cli.OptionValidator": "src.main.org.apache.commons.cli.OptionValidator.OptionValidator",
    "src.main.org.apache.commons.cli.PosixParser": "src.main.org.apache.commons.cli.PosixParser.PosixParser",
    "src.main.org.apache.commons.cli.ParseException": "src.main.org.apache.commons.cli.ParseException.ParseException",
    "src.main.org.apache.commons.cli.CommandLineParser": "src.main.org.apache.commons.cli.CommandLineParser.CommandLineParser",
    "src.main.org.apache.commons.cli.OptionBuilder": "src.main.org.apache.commons.cli.OptionBuilder.OptionBuilder",
    "src.main.org.apache.commons.cli.Options": "src.main.org.apache.commons.cli.Options.Options",
    "src.main.org.apache.commons.cli.Option": "src.main.org.apache.commons.cli.Option.Option",
    "src.main.org.apache.commons.cli.UnrecognizedOptionException": "src.main.org.apache.commons.cli.UnrecognizedOptionException.UnrecognizedOptionException",
    "src.main.org.apache.commons.cli.MissingArgumentException": "src.main.org.apache.commons.cli.MissingArgumentException.MissingArgumentException",
    "src.main.org.apache.commons.cli.GnuParser": "src.main.org.apache.commons.cli.GnuParser.GnuParser",
    "src.main.org.apache.commons.cli.AmbiguousOptionException": "src.main.org.apache.commons.cli.AmbiguousOptionException.AmbiguousOptionException",
    "src.main.org.apache.commons.cli.BasicParser": "src.main.org.apache.commons.cli.BasicParser.BasicParser",
    "src.main.org.apache.commons.cli.PatternOptionBuilder": "src.main.org.apache.commons.cli.PatternOptionBuilder.PatternOptionBuilder",
    "src.main.org.apache.commons.cli.DefaultParser": "src.main.org.apache.commons.cli.DefaultParser.DefaultParser",
    "src.main.org.apache.commons.cli.HelpFormatter": "src.main.org.apache.commons.cli.HelpFormatter.HelpFormatter",
    "src.main.org.apache.commons.cli.CommandLine": "src.main.org.apache.commons.cli.CommandLine.CommandLine",
    "src.main.org.apache.commons.cli.OptionGroup": "src.main.org.apache.commons.cli.OptionGroup.OptionGroup",
    "src.main.org.apache.commons.cli.AlreadySelectedException": "src.main.org.apache.commons.cli.AlreadySelectedException.AlreadySelectedException",
    "src.main.org.apache.commons.cli.Util": "src.main.org.apache.commons.cli.Util.Util",
    "src.main.org.apache.commons.cli.Parser": "src.main.org.apache.commons.cli.Parser.Parser",
    "src.main.org.apache.commons.cli.DefaultParser$Builder": "src.main.org.apache.commons.cli.DefaultParser.Builder",
    "src.main.org.apache.commons.cli.HelpFormatterTest$1": "HelpFormatterTest_AnonymousClass_1",
    "src.test.org.apache.commons.cli.OptionTest$DefaultOption": "src.test.org.apache.commons.cli.OptionTest.DefaultOption",
    "src.test.org.apache.commons.cli.OptionTest$TestOption": "src.test.org.apache.commons.cli.OptionTest.TestOption",
    "src.test.org.apache.commons.cli.TypeHandlerTest$NotInstantiable": "src.test.org.apache.commons.cli.TypeHandlerTest.NotInstantiable",
    "src.test.org.apache.commons.cli.TypeHandlerTest$Instantiable": "src.test.org.apache.commons.cli.TypeHandlerTest.Instantiable",
    "java.io.StringReader": "io.StringIO",
    "java.lang.StringBuilder": "io.StringIO",
    "java.io.BufferedReader": "io.BufferedReader",
    "java.lang.CharSequence": "str",
    "java.util.stream.Stream": "PeekableIterator",
    "java.io.InputStreamReader": "io.TextIOWrapper",
    "java.io.OutputStreamWriter": "io.TextIOWrapper",
    "java.io.StringWriter": "io.StringIO",
    "java.io.PipedReader": "io.BytesIO",
    "java.io.PipedWriter": "io.BytesIO",
    "java.io.FilterInputStream": "io.BufferedReader",
    "java.io.FilterOutputStream": "io.BufferedWriter",
    "java.io.PipedInputStream": "io.BytesIO",
    "java.io.PipedOutputStream": "io.BytesIO",
    "java.io.PrintStream": "io.BytesIO",
    "java.util.concurrent.ThreadFactory": "threading.Thread",
    "java.util.concurrent.Executors$DefaultThreadFactory": "threading.Thread",
    "src.main.org.apache.commons.csv.Constants": "src.main.org.apache.commons.csv.Constants.Constants",
    "src.main.org.apache.commons.csv.CSVFormat": "src.main.org.apache.commons.csv.CSVFormat.CSVFormat",
    "src.main.org.apache.commons.csv.CSVFormat$Builder": "src.main.org.apache.commons.csv.CSVFormat.Builder",
    "src.main.org.apache.commons.csv.CSVFormat$Predefined": "src.main.org.apache.commons.csv.CSVFormat.Predefined",
    "src.main.org.apache.commons.csv.CSVParser": "src.main.org.apache.commons.csv.CSVParser.CSVParser",
    "src.main.org.apache.commons.csv.CSVParser$CSVRecordIterator": "src.main.org.apache.commons.csv.CSVParser.CSVRecordIterator",
    "src.main.org.apache.commons.csv.CSVParser$Headers": "src.main.org.apache.commons.csv.CSVParser.Headers",
    "src.main.org.apache.commons.csv.CSVPrinter": "src.main.org.apache.commons.csv.CSVPrinter.CSVPrinter",
    "src.main.org.apache.commons.csv.CSVRecord": "src.main.org.apache.commons.csv.CSVRecord.CSVRecord",
    "src.main.org.apache.commons.csv.DuplicateHeaderMode": "src.main.org.apache.commons.csv.DuplicateHeaderMode.DuplicateHeaderMode",
    "src.main.org.apache.commons.csv.ExtendedBufferedReader": "src.main.org.apache.commons.csv.ExtendedBufferedReader.ExtendedBufferedReader",
    "src.main.org.apache.commons.csv.IOUtils": "src.main.org.apache.commons.csv.IOUtils.IOUtils",
    "src.main.org.apache.commons.csv.Lexer": "src.main.org.apache.commons.csv.Lexer.Lexer",
    "src.main.org.apache.commons.csv.QuoteMode": "src.main.org.apache.commons.csv.QuoteMode.QuoteMode",
    "src.main.org.apache.commons.csv.Token": "src.main.org.apache.commons.csv.Token.Token",
    "src.main.org.apache.commons.csv.Token$Type": "src.main.org.apache.commons.csv.Token.Type",
    "src.test.org.apache.commons.csv.PerformanceTest$CSVParserFactory": "src.test.org.apache.commons.csv.PerformanceTest.CSVParserFactory",
    "src.test.org.apache.commons.csv.PerformanceTest$Stats": "src.test.org.apache.commons.csv.PerformanceTest.Stats",
    "java.math.BigInteger": "int",
    "java.math.BigDecimal": "float",
    "src.main.org.apache.commons.graph.builder.AbstractGraphConnection": "src.main.org.apache.commons.graph.builder.AbstractGraphConnection.AbstractGraphConnection",
    "src.main.org.apache.commons.graph.builder.DefaultGrapher": "src.main.org.apache.commons.graph.builder.DefaultGrapher.DefaultGrapher",
    "src.main.org.apache.commons.graph.builder.DefaultHeadVertexConnector": "src.main.org.apache.commons.graph.builder.DefaultHeadVertexConnector.DefaultHeadVertexConnector",
    "src.main.org.apache.commons.graph.builder.DefaultLinkedConnectionBuilder": "src.main.org.apache.commons.graph.builder.DefaultLinkedConnectionBuilder.DefaultLinkedConnectionBuilder",
    "src.main.org.apache.commons.graph.builder.DefaultTailVertexConnector": "src.main.org.apache.commons.graph.builder.DefaultTailVertexConnector.DefaultTailVertexConnector",
    "src.main.org.apache.commons.graph.builder.GraphConnection": "src.main.org.apache.commons.graph.builder.GraphConnection.GraphConnection",
    "src.main.org.apache.commons.graph.builder.GraphConnector": "src.main.org.apache.commons.graph.builder.GraphConnector.GraphConnector",
    "src.main.org.apache.commons.graph.builder.HeadVertexConnector": "src.main.org.apache.commons.graph.builder.HeadVertexConnector.HeadVertexConnector",
    "src.main.org.apache.commons.graph.builder.LinkedConnectionBuilder": "src.main.org.apache.commons.graph.builder.LinkedConnectionBuilder.LinkedConnectionBuilder",
    "src.main.org.apache.commons.graph.builder.TailVertexConnector": "src.main.org.apache.commons.graph.builder.TailVertexConnector.TailVertexConnector",
    "src.main.org.apache.commons.graph.collections.DisjointSet": "src.main.org.apache.commons.graph.collections.DisjointSet.DisjointSet",
    "src.main.org.apache.commons.graph.collections.DisjointSetNode": "src.main.org.apache.commons.graph.collections.DisjointSetNode.DisjointSetNode",
    "src.main.org.apache.commons.graph.collections.FibonacciHeap": "src.main.org.apache.commons.graph.collections.FibonacciHeap.FibonacciHeap",
    "src.main.org.apache.commons.graph.collections.FibonacciHeapNode": "src.main.org.apache.commons.graph.collections.FibonacciHeap.FibonacciHeapNode",
    "src.main.org.apache.commons.graph.coloring.ColoredVertices": "src.main.org.apache.commons.graph.coloring.ColoredVertices.ColoredVertices",
    "src.main.org.apache.commons.graph.coloring.ColoringAlgorithmsSelector": "src.main.org.apache.commons.graph.coloring.ColoringAlgorithmsSelector.ColoringAlgorithmsSelector",
    "src.main.org.apache.commons.graph.coloring.ColorsBuilder": "src.main.org.apache.commons.graph.coloring.ColorsBuilder.ColorsBuilder",
    "src.main.org.apache.commons.graph.coloring.DefaultColoringAlgorithmsSelector": "src.main.org.apache.commons.graph.coloring.DefaultColoringAlgorithmsSelector.DefaultColoringAlgorithmsSelector",
    "src.main.org.apache.commons.graph.coloring.DefaultColorsBuilder": "src.main.org.apache.commons.graph.coloring.DefaultColorsBuilder.DefaultColorsBuilder",
    "src.main.org.apache.commons.graph.coloring.NotEnoughColorsException": "src.main.org.apache.commons.graph.coloring.NotEnoughColorsException.NotEnoughColorsException",
    "src.main.org.apache.commons.graph.coloring.UncoloredOrderedVertices": "src.main.org.apache.commons.graph.coloring.UncoloredOrderedVertices.UncoloredOrderedVertices",
    "src.main.org.apache.commons.graph.connectivity.ConnectedComponentHandler": "src.main.org.apache.commons.graph.connectivity.ConnectedComponentHandler.ConnectedComponentHandler",
    "src.main.org.apache.commons.graph.connectivity.ConnectivityAlgorithmsSelector": "src.main.org.apache.commons.graph.connectivity.ConnectivityAlgorithmsSelector.ConnectivityAlgorithmsSelector",
    "src.main.org.apache.commons.graph.connectivity.ConnectivityBuilder": "src.main.org.apache.commons.graph.connectivity.ConnectivityBuilder.ConnectivityBuilder",
    "src.main.org.apache.commons.graph.connectivity.DefaultConnectivityAlgorithmsSelector": "src.main.org.apache.commons.graph.connectivity.DefaultConnectivityAlgorithmsSelector.DefaultConnectivityAlgorithmsSelector",
    "src.main.org.apache.commons.graph.connectivity.DefaultConnectivityBuilder": "src.main.org.apache.commons.graph.connectivity.DefaultConnectivityBuilder.DefaultConnectivityBuilder",
    "src.main.org.apache.commons.graph.elo.Category": "src.main.org.apache.commons.graph.elo.Category.Category",
    "src.main.org.apache.commons.graph.elo.DefaultKFactorBuilder": "src.main.org.apache.commons.graph.elo.DefaultKFactorBuilder.DefaultKFactorBuilder",
    "src.main.org.apache.commons.graph.elo.DefaultRankingSelector": "src.main.org.apache.commons.graph.elo.DefaultRankingSelector.DefaultRankingSelector",
    "src.main.org.apache.commons.graph.elo.GameResult": "src.main.org.apache.commons.graph.elo.GameResult.GameResult",
    "src.main.org.apache.commons.graph.elo.KFactorBuilder": "src.main.org.apache.commons.graph.elo.KFactorBuilder.KFactorBuilder",
    "src.main.org.apache.commons.graph.elo.PlayersRank": "src.main.org.apache.commons.graph.elo.PlayersRank.PlayersRank",
    "src.main.org.apache.commons.graph.elo.RankingSelector": "src.main.org.apache.commons.graph.elo.RankingSelector.RankingSelector",
    "src.main.org.apache.commons.graph.export.AbstractExporter": "src.main.org.apache.commons.graph.export.AbstractExporter.AbstractExporter",
    "src.main.org.apache.commons.graph.export.DefaultExportSelector": "src.main.org.apache.commons.graph.export.DefaultExportSelector.DefaultExportSelector",
    "src.main.org.apache.commons.graph.export.DotExporter": "src.main.org.apache.commons.graph.export.DotExporter.DotExporter",
    "src.main.org.apache.commons.graph.export.ExportSelector": "src.main.org.apache.commons.graph.export.ExportSelector.ExportSelector",
    "src.main.org.apache.commons.graph.export.GraphExportException": "src.main.org.apache.commons.graph.export.GraphExportException.GraphExportException",
    "src.main.org.apache.commons.graph.export.NamedExportSelector": "src.main.org.apache.commons.graph.export.NamedExportSelector.NamedExportSelector",
    "src.main.org.apache.commons.graph.flow.DefaultFlowWeightedEdgesBuilder": "src.main.org.apache.commons.graph.flow.DefaultFlowWeightedEdgesBuilder.DefaultFlowWeightedEdgesBuilder",
    "src.main.org.apache.commons.graph.flow.DefaultFromHeadBuilder": "src.main.org.apache.commons.graph.flow.DefaultFromHeadBuilder.DefaultFromHeadBuilder",
    "src.main.org.apache.commons.graph.flow.DefaultMaxFlowAlgorithmSelector": "src.main.org.apache.commons.graph.flow.DefaultMaxFlowAlgorithmSelector.DefaultMaxFlowAlgorithmSelector",
    "src.main.org.apache.commons.graph.flow.DefaultToTailBuilder": "src.main.org.apache.commons.graph.flow.DefaultToTailBuilder.DefaultToTailBuilder",
    "src.main.org.apache.commons.graph.flow.FlowNetworkHandler": "src.main.org.apache.commons.graph.flow.FlowNetworkHandler.FlowNetworkHandler",
    "src.main.org.apache.commons.graph.flow.FlowWeightedEdgesBuilder": "src.main.org.apache.commons.graph.flow.FlowWeightedEdgesBuilder.FlowWeightedEdgesBuilder",
    "src.main.org.apache.commons.graph.flow.FromHeadBuilder": "src.main.org.apache.commons.graph.flow.FromHeadBuilder.FromHeadBuilder",
    "src.main.org.apache.commons.graph.flow.MaxFlowAlgorithmSelector": "src.main.org.apache.commons.graph.flow.MaxFlowAlgorithmSelector.MaxFlowAlgorithmSelector",
    "src.main.org.apache.commons.graph.flow.ToTailBuilder": "src.main.org.apache.commons.graph.flow.ToTailBuilder.ToTailBuilder",
    "src.main.org.apache.commons.graph.model.BaseGraph": "src.main.org.apache.commons.graph.model.BaseGraph.BaseGraph",
    "src.main.org.apache.commons.graph.model.BaseMutableGraph": "src.main.org.apache.commons.graph.model.BaseMutableGraph.BaseMutableGraph",
    "src.main.org.apache.commons.graph.model.DirectedMutableGraph": "src.main.org.apache.commons.graph.model.DirectedMutableGraph.DirectedMutableGraph",
    "src.main.org.apache.commons.graph.model.InMemoryPath": "src.main.org.apache.commons.graph.model.InMemoryPath.InMemoryPath",
    "src.main.org.apache.commons.graph.model.InMemoryWeightedPath": "src.main.org.apache.commons.graph.model.InMemoryWeightedPath.InMemoryWeightedPath",
    "src.main.org.apache.commons.graph.model.MutableSpanningTree": "src.main.org.apache.commons.graph.model.MutableSpanningTree.MutableSpanningTree",
    "src.main.org.apache.commons.graph.model.RevertedGraph": "src.main.org.apache.commons.graph.model.RevertedGraph.RevertedGraph",
    "src.main.org.apache.commons.graph.model.UndirectedMutableGraph": "src.main.org.apache.commons.graph.model.UndirectedMutableGraph.UndirectedMutableGraph",
    "src.main.org.apache.commons.graph.scc.CheriyanMehlhornGabowAlgorithm": "src.main.org.apache.commons.graph.scc.CheriyanMehlhornGabowAlgorithm.CheriyanMehlhornGabowAlgorithm",
    "src.main.org.apache.commons.graph.scc.DefaultSccAlgorithmSelector": "src.main.org.apache.commons.graph.scc.DefaultSccAlgorithmSelector.DefaultSccAlgorithmSelector",
    "src.main.org.apache.commons.graph.scc.KosarajuSharirAlgorithm": "src.main.org.apache.commons.graph.scc.KosarajuSharirAlgorithm.KosarajuSharirAlgorithm",
    "src.main.org.apache.commons.graph.scc.SccAlgorithm": "src.main.org.apache.commons.graph.scc.SccAlgorithm.SccAlgorithm",
    "src.main.org.apache.commons.graph.scc.SccAlgorithmSelector": "src.main.org.apache.commons.graph.scc.SccAlgorithmSelector.SccAlgorithmSelector",
    "src.main.org.apache.commons.graph.scc.TarjanAlgorithm": "src.main.org.apache.commons.graph.scc.TarjanAlgorithm.TarjanAlgorithm",
    "src.main.org.apache.commons.graph.scc.TarjanVertexMetaInfo": "src.main.org.apache.commons.graph.scc.TarjanVertexMetaInfo.TarjanVertexMetaInfo",
    "src.main.org.apache.commons.graph.shortestpath.AllVertexPairsShortestPath": "src.main.org.apache.commons.graph.shortestpath.AllVertexPairsShortestPath.AllVertexPairsShortestPath",
    "src.main.org.apache.commons.graph.shortestpath.DefaultHeuristicBuilder": "src.main.org.apache.commons.graph.shortestpath.DefaultHeuristicBuilder.DefaultHeuristicBuilder",
    "src.main.org.apache.commons.graph.shortestpath.DefaultPathSourceSelector": "src.main.org.apache.commons.graph.shortestpath.DefaultPathSourceSelector.DefaultPathSourceSelector",
    "src.main.org.apache.commons.graph.shortestpath.DefaultShortestPathAlgorithmSelector": "src.main.org.apache.commons.graph.shortestpath.DefaultShortestPathAlgorithmSelector.DefaultShortestPathAlgorithmSelector",
    "src.main.org.apache.commons.graph.shortestpath.DefaultTargetSourceSelector": "src.main.org.apache.commons.graph.shortestpath.DefaultTargetSourceSelector.DefaultTargetSourceSelector",
    "src.main.org.apache.commons.graph.shortestpath.DefaultWeightedEdgesSelector": "src.main.org.apache.commons.graph.shortestpath.DefaultWeightedEdgesSelector.DefaultWeightedEdgesSelector",
    "src.main.org.apache.commons.graph.shortestpath.Heuristic": "src.main.org.apache.commons.graph.shortestpath.Heuristic.Heuristic",
    "src.main.org.apache.commons.graph.shortestpath.HeuristicBuilder": "src.main.org.apache.commons.graph.shortestpath.HeuristicBuilder.HeuristicBuilder",
    "src.main.org.apache.commons.graph.shortestpath.NegativeWeightedCycleException": "src.main.org.apache.commons.graph.shortestpath.NegativeWeightedCycleException.NegativeWeightedCycleException",
    "src.main.org.apache.commons.graph.shortestpath.PathNotFoundException": "src.main.org.apache.commons.graph.shortestpath.PathNotFoundException.PathNotFoundException",
    "src.main.org.apache.commons.graph.shortestpath.PathSourceSelector": "src.main.org.apache.commons.graph.shortestpath.PathSourceSelector.PathSourceSelector",
    "src.main.org.apache.commons.graph.shortestpath.PathWeightedEdgesBuilder": "src.main.org.apache.commons.graph.shortestpath.PathWeightedEdgesBuilder.PathWeightedEdgesBuilder",
    "src.main.org.apache.commons.graph.shortestpath.PredecessorsList": "src.main.org.apache.commons.graph.shortestpath.PredecessorsList.PredecessorsList",
    "src.main.org.apache.commons.graph.shortestpath.ShortestDistances": "src.main.org.apache.commons.graph.shortestpath.ShortestDistances.ShortestDistances",
    "src.main.org.apache.commons.graph.shortestpath.ShortestPathAlgorithmSelector": "src.main.org.apache.commons.graph.shortestpath.ShortestPathAlgorithmSelector.ShortestPathAlgorithmSelector",
    "src.main.org.apache.commons.graph.shortestpath.TargetSourceSelector": "src.main.org.apache.commons.graph.shortestpath.TargetSourceSelector.TargetSourceSelector",
    "src.main.org.apache.commons.graph.spanning.DefaultSpanningTreeAlgorithmSelector": "src.main.org.apache.commons.graph.spanning.DefaultSpanningTreeAlgorithmSelector.DefaultSpanningTreeAlgorithmSelector",
    "src.main.org.apache.commons.graph.spanning.DefaultSpanningTreeSourceSelector": "src.main.org.apache.commons.graph.spanning.DefaultSpanningTreeSourceSelector.DefaultSpanningTreeSourceSelector",
    "src.main.org.apache.commons.graph.spanning.DefaultSpanningWeightedEdgeMapperBuilder": "src.main.org.apache.commons.graph.spanning.DefaultSpanningWeightedEdgeMapperBuilder.DefaultSpanningWeightedEdgeMapperBuilder",
    "src.main.org.apache.commons.graph.spanning.ReverseDeleteGraph": "src.main.org.apache.commons.graph.spanning.ReverseDeleteGraph.ReverseDeleteGraph",
    "src.main.org.apache.commons.graph.spanning.ShortestEdges": "src.main.org.apache.commons.graph.spanning.ShortestEdges.ShortestEdges",
    "src.main.org.apache.commons.graph.spanning.SpanningTreeAlgorithmSelector": "src.main.org.apache.commons.graph.spanning.SpanningTreeAlgorithmSelector.SpanningTreeAlgorithmSelector",
    "src.main.org.apache.commons.graph.spanning.SpanningTreeSourceSelector": "src.main.org.apache.commons.graph.spanning.SpanningTreeSourceSelector.SpanningTreeSourceSelector",
    "src.main.org.apache.commons.graph.spanning.SpanningWeightedEdgeMapperBuilder": "src.main.org.apache.commons.graph.spanning.SpanningWeightedEdgeMapperBuilder.SpanningWeightedEdgeMapperBuilder",
    "src.main.org.apache.commons.graph.spanning.SuperVertex": "src.main.org.apache.commons.graph.spanning.SuperVertex.SuperVertex",
    "src.main.org.apache.commons.graph.spanning.WeightedEdgesComparator": "src.main.org.apache.commons.graph.spanning.WeightedEdgesComparator.WeightedEdgesComparator",
    "src.main.org.apache.commons.graph.utils.Assertions": "src.main.org.apache.commons.graph.utils.Assertions.Assertions",
    "src.main.org.apache.commons.graph.utils.Objects": "src.main.org.apache.commons.graph.utils.Objects.Objects",
    "src.main.org.apache.commons.graph.visit.BaseGraphVisitHandler": "src.main.org.apache.commons.graph.visit.BaseGraphVisitHandler.BaseGraphVisitHandler",
    "src.main.org.apache.commons.graph.visit.DefaultVisitAlgorithmsSelector": "src.main.org.apache.commons.graph.visit.DefaultVisitAlgorithmsSelector.DefaultVisitAlgorithmsSelector",
    "src.main.org.apache.commons.graph.visit.DefaultVisitSourceSelector": "src.main.org.apache.commons.graph.visit.DefaultVisitSourceSelector.DefaultVisitSourceSelector",
    "src.main.org.apache.commons.graph.visit.GraphVisitHandler": "src.main.org.apache.commons.graph.visit.GraphVisitHandler.GraphVisitHandler",
    "src.main.org.apache.commons.graph.visit.VisitAlgorithmsSelector": "src.main.org.apache.commons.graph.visit.VisitAlgorithmsSelector.VisitAlgorithmsSelector",
    "src.main.org.apache.commons.graph.visit.VisitGraphBuilder": "src.main.org.apache.commons.graph.visit.VisitGraphBuilder.VisitGraphBuilder",
    "src.main.org.apache.commons.graph.visit.VisitSourceSelector": "src.main.org.apache.commons.graph.visit.VisitSourceSelector.VisitSourceSelector",
    "src.main.org.apache.commons.graph.visit.VisitState": "src.main.org.apache.commons.graph.visit.VisitState.VisitState",
    "src.main.org.apache.commons.graph.weight.primitive.BigDecimalWeightBaseOperations": "src.main.org.apache.commons.graph.weight.primitive.BigDecimalWeightBaseOperations.BigDecimalWeightBaseOperations",
    "src.main.org.apache.commons.graph.weight.primitive.BigIntegerWeightBaseOperations": "src.main.org.apache.commons.graph.weight.primitive.BigIntegerWeightBaseOperations.BigIntegerWeightBaseOperations",
    "src.main.org.apache.commons.graph.weight.primitive.DoubleWeightBaseOperations": "src.main.org.apache.commons.graph.weight.primitive.DoubleWeightBaseOperations.DoubleWeightBaseOperations",
    "src.main.org.apache.commons.graph.weight.primitive.FloatWeightBaseOperations": "src.main.org.apache.commons.graph.weight.primitive.FloatWeightBaseOperations.FloatWeightBaseOperations",
    "src.main.org.apache.commons.graph.weight.primitive.IntegerWeightBaseOperations": "src.main.org.apache.commons.graph.weight.primitive.IntegerWeightBaseOperations.IntegerWeightBaseOperations",
    "src.main.org.apache.commons.graph.weight.primitive.LongWeightBaseOperations": "src.main.org.apache.commons.graph.weight.primitive.LongWeightBaseOperations.LongWeightBaseOperations",
    "src.main.org.apache.commons.graph.weight.Monoid": "src.main.org.apache.commons.graph.weight.Monoid.Monoid",
    "src.main.org.apache.commons.graph.weight.OrderedMonoid": "src.main.org.apache.commons.graph.weight.OrderedMonoid.OrderedMonoid",
    "src.main.org.apache.commons.graph.CommonsGraph": "src.main.org.apache.commons.graph.CommonsGraph.CommonsGraph",
    "src.main.org.apache.commons.graph.DirectedGraph": "src.main.org.apache.commons.graph.DirectedGraph.DirectedGraph",
    "src.main.org.apache.commons.graph.Graph": "src.main.org.apache.commons.graph.Graph.Graph",
    "src.main.org.apache.commons.graph.GraphException": "src.main.org.apache.commons.graph.GraphException.GraphException",
    "src.main.org.apache.commons.graph.Mapper": "src.main.org.apache.commons.graph.Mapper.Mapper",
    "src.main.org.apache.commons.graph.MutableGraph": "src.main.org.apache.commons.graph.MutableGraph.MutableGraph",
    "src.main.org.apache.commons.graph.Path": "src.main.org.apache.commons.graph.Path.Path",
    "src.main.org.apache.commons.graph.SpanningTree": "src.main.org.apache.commons.graph.SpanningTree.SpanningTree",
    "src.main.org.apache.commons.graph.SynchronizedDirectedGraph": "src.main.org.apache.commons.graph.SynchronizedDirectedGraph.SynchronizedDirectedGraph",
    "src.main.org.apache.commons.graph.SynchronizedGraph": "src.main.org.apache.commons.graph.SynchronizedGraph.SynchronizedGraph",
    "src.main.org.apache.commons.graph.SynchronizedMutableGraph": "src.main.org.apache.commons.graph.SynchronizedMutableGraph.SynchronizedMutableGraph",
    "src.main.org.apache.commons.graph.SynchronizedUndirectedGraph": "src.main.org.apache.commons.graph.SynchronizedUndirectedGraph.SynchronizedUndirectedGraph",
    "src.main.org.apache.commons.graph.UndirectedGraph": "src.main.org.apache.commons.graph.UndirectedGraph.UndirectedGraph",
    "src.main.org.apache.commons.graph.VertexPair": "src.main.org.apache.commons.graph.VertexPair.VertexPair",
    "src.main.org.apache.commons.graph.Weighted": "src.main.org.apache.commons.graph.Weighted.Weighted",
    "src.main.org.apache.commons.graph.WeightedPath": "src.main.org.apache.commons.graph.WeightedPath.WeightedPath",
    "src.test.org.apache.commons.graph.elo.SimplePlayersRank": "src.test.org.apache.commons.graph.elo.SimplePlayersRank.SimplePlayersRank",
    "src.test.org.apache.commons.graph.export.EdgeLabelMapper": "src.test.org.apache.commons.graph.export.EdgeLabelMapper.EdgeLabelMapper",
    "src.test.org.apache.commons.graph.export.EdgeWeightMapper": "src.test.org.apache.commons.graph.export.EdgeWeightMapper.EdgeWeightMapper",
    "src.test.org.apache.commons.graph.export.VertexLabelMapper": "src.test.org.apache.commons.graph.export.VertexLabelMapper.VertexLabelMapper",
    "src.test.org.apache.commons.graph.model.BaseLabeledEdge": "src.test.org.apache.commons.graph.model.BaseLabeledEdge.BaseLabeledEdge",
    "src.test.org.apache.commons.graph.model.BaseLabeledVertex": "src.test.org.apache.commons.graph.model.BaseLabeledVertex.BaseLabeledVertex",
    "src.test.org.apache.commons.graph.model.BaseLabeledWeightedEdge": "src.test.org.apache.commons.graph.model.BaseLabeledWeightedEdge.BaseLabeledWeightedEdge",
    "src.test.org.apache.commons.graph.model.BaseMutableGraphTestCase$GraphInsert": "src.test.org.apache.commons.graph.model.BaseMutableGraphTestCase.GraphInsert",
    "src.test.org.apache.commons.graph.model.BaseWeightedEdge": "src.test.org.apache.commons.graph.model.BaseWeightedEdge.BaseWeightedEdge",
    "src.test.org.apache.commons.graph.utils.GraphUtils": "src.test.org.apache.commons.graph.utils.GraphUtils.GraphUtils",
    "src.test.org.apache.commons.graph.utils.MultiThreadedTestRunner": "src.test.org.apache.commons.graph.utils.MultiThreadedTestRunner.MultiThreadedTestRunner",
    "src.test.org.apache.commons.graph.utils.TestRunner": "src.test.org.apache.commons.graph.utils.TestRunner.TestRunner",
    "src.test.org.apache.commons.graph.visit.NodeSequenceVisitor": "src.test.org.apache.commons.graph.visit.NodeSequenceVisitor.NodeSequenceVisitor",

    "src.main.org.apache.commons.validator.routines.checkdigit.ABANumberCheckDigit": "src.main.org.apache.commons.validator.routines.checkdigit.ABANumberCheckDigit.ABANumberCheckDigit",
    "src.main.org.apache.commons.validator.routines.checkdigit.CUSIPCheckDigit": "src.main.org.apache.commons.validator.routines.checkdigit.CUSIPCheckDigit.CUSIPCheckDigit",
    "src.main.org.apache.commons.validator.routines.checkdigit.CheckDigit": "src.main.org.apache.commons.validator.routines.checkdigit.CheckDigit.CheckDigit",
    "src.main.org.apache.commons.validator.routines.checkdigit.CheckDigitException": "src.main.org.apache.commons.validator.routines.checkdigit.CheckDigitException.CheckDigitException",
    "src.main.org.apache.commons.validator.routines.checkdigit.EAN13CheckDigit": "src.main.org.apache.commons.validator.routines.checkdigit.EAN13CheckDigit.EAN13CheckDigit",
    "src.main.org.apache.commons.validator.routines.checkdigit.IBANCheckDigit": "src.main.org.apache.commons.validator.routines.checkdigit.IBANCheckDigit.IBANCheckDigit",
    "src.main.org.apache.commons.validator.routines.checkdigit.ISBN10CheckDigit": "src.main.org.apache.commons.validator.routines.checkdigit.ISBN10CheckDigit.ISBN10CheckDigit",
    "src.main.org.apache.commons.validator.routines.checkdigit.ISBNCheckDigit": "src.main.org.apache.commons.validator.routines.checkdigit.ISBNCheckDigit.ISBNCheckDigit",
    "src.main.org.apache.commons.validator.routines.checkdigit.ISINCheckDigit": "src.main.org.apache.commons.validator.routines.checkdigit.ISINCheckDigit.ISINCheckDigit",
    "src.main.org.apache.commons.validator.routines.checkdigit.ISSNCheckDigit": "src.main.org.apache.commons.validator.routines.checkdigit.ISSNCheckDigit.ISSNCheckDigit",
    "src.main.org.apache.commons.validator.routines.checkdigit.LuhnCheckDigit": "src.main.org.apache.commons.validator.routines.checkdigit.LuhnCheckDigit.LuhnCheckDigit",
    "src.main.org.apache.commons.validator.routines.checkdigit.ModulusCheckDigit": "src.main.org.apache.commons.validator.routines.checkdigit.ModulusCheckDigit.ModulusCheckDigit",
    "src.main.org.apache.commons.validator.routines.checkdigit.ModulusTenCheckDigit": "src.main.org.apache.commons.validator.routines.checkdigit.ModulusCheckDigit.ModulusTenCheckDigit",
    "src.main.org.apache.commons.validator.routines.checkdigit.SedolCheckDigit": "src.main.org.apache.commons.validator.routines.checkdigit.SedolCheckDigit.SedolCheckDigit",
    "src.main.org.apache.commons.validator.routines.checkdigit.VerhoeffCheckDigit": "src.main.org.apache.commons.validator.routines.checkdigit.VerhoeffCheckDigit.VerhoeffCheckDigit",
    "src.main.org.apache.commons.validator.routines.AbstractCalendarValidator": "src.main.org.apache.commons.validator.routines.AbstractCalendarValidator.AbstractCalendarValidator",
    "src.main.org.apache.commons.validator.routines.AbstractFormatValidator": "src.main.org.apache.commons.validator.routines.AbstractFormatValidator.AbstractFormatValidator",
    "src.main.org.apache.commons.validator.routines.AbstractNumberValidator": "src.main.org.apache.commons.validator.routines.AbstractNumberValidator.AbstractNumberValidator",
    "src.main.org.apache.commons.validator.routines.BigDecimalValidator": "src.main.org.apache.commons.validator.routines.BigDecimalValidator.BigDecimalValidator",
    "src.main.org.apache.commons.validator.routines.BigIntegerValidator": "src.main.org.apache.commons.validator.routines.BigIntegerValidator.BigIntegerValidator",
    "src.main.org.apache.commons.validator.routines.ByteValidator": "src.main.org.apache.commons.validator.routines.ByteValidator.ByteValidator",
    "src.main.org.apache.commons.validator.routines.CalendarValidator": "src.main.org.apache.commons.validator.routines.CalendarValidator.CalendarValidator",
    "src.main.org.apache.commons.validator.routines.CodeValidator": "src.main.org.apache.commons.validator.routines.CodeValidator.CodeValidator",
    "src.main.org.apache.commons.validator.routines.CreditCardValidator": "src.main.org.apache.commons.validator.routines.CreditCardValidator.CreditCardValidator",
    "src.main.org.apache.commons.validator.routines.CurrencyValidator": "src.main.org.apache.commons.validator.routines.CurrencyValidator.CurrencyValidator",
    "src.main.org.apache.commons.validator.routines.DateValidator": "src.main.org.apache.commons.validator.routines.DateValidator.DateValidator",
    "src.main.org.apache.commons.validator.routines.DomainValidator": "src.main.org.apache.commons.validator.routines.DomainValidator.DomainValidator",
    "src.main.org.apache.commons.validator.routines.DoubleValidator": "src.main.org.apache.commons.validator.routines.DoubleValidator.DoubleValidator",
    "src.main.org.apache.commons.validator.routines.EmailValidator": "src.main.org.apache.commons.validator.routines.EmailValidator.EmailValidator",
    "src.main.org.apache.commons.validator.routines.FloatValidator": "src.main.org.apache.commons.validator.routines.FloatValidator.FloatValidator",
    "src.main.org.apache.commons.validator.routines.IBANValidator": "src.main.org.apache.commons.validator.routines.IBANValidator.IBANValidator",
    "src.main.org.apache.commons.validator.routines.ISBNValidator": "src.main.org.apache.commons.validator.routines.ISBNValidator.ISBNValidator",
    "src.main.org.apache.commons.validator.routines.ISINValidator": "src.main.org.apache.commons.validator.routines.ISINValidator.ISINValidator",
    "src.main.org.apache.commons.validator.routines.ISSNValidator": "src.main.org.apache.commons.validator.routines.ISSNValidator.ISSNValidator",
    "src.main.org.apache.commons.validator.routines.InetAddressValidator": "src.main.org.apache.commons.validator.routines.InetAddressValidator.InetAddressValidator",
    "src.main.org.apache.commons.validator.routines.IntegerValidator": "src.main.org.apache.commons.validator.routines.IntegerValidator.IntegerValidator",
    "src.main.org.apache.commons.validator.routines.LongValidator": "src.main.org.apache.commons.validator.routines.LongValidator.LongValidator",
    "src.main.org.apache.commons.validator.routines.PercentValidator": "src.main.org.apache.commons.validator.routines.PercentValidator.PercentValidator",
    "src.main.org.apache.commons.validator.routines.RegexValidator": "src.main.org.apache.commons.validator.routines.RegexValidator.RegexValidator",
    "src.main.org.apache.commons.validator.routines.ShortValidator": "src.main.org.apache.commons.validator.routines.ShortValidator.ShortValidator",
    "src.main.org.apache.commons.validator.routines.TimeValidator": "src.main.org.apache.commons.validator.routines.TimeValidator.TimeValidator",
    "src.main.org.apache.commons.validator.routines.UrlValidator": "src.main.org.apache.commons.validator.routines.UrlValidator.UrlValidator",
    "src.main.org.apache.commons.validator.Arg": "src.main.org.apache.commons.validator.Arg.Arg",
    "src.main.org.apache.commons.validator.CreditCardValidator": "src.main.org.apache.commons.validator.CreditCardValidator.CreditCardValidator",
    "src.main.org.apache.commons.validator.DateValidator": "src.main.org.apache.commons.validator.DateValidator.DateValidator",
    "src.main.org.apache.commons.validator.EmailValidator": "src.main.org.apache.commons.validator.EmailValidator.EmailValidator",
    "src.main.org.apache.commons.validator.Field": "src.main.org.apache.commons.validator.Field.Field",
    "src.main.org.apache.commons.validator.Form": "src.main.org.apache.commons.validator.Form.Form",
    "src.main.org.apache.commons.validator.FormSet": "src.main.org.apache.commons.validator.FormSet.FormSet",
    "src.main.org.apache.commons.validator.GenericTypeValidator": "src.main.org.apache.commons.validator.GenericTypeValidator.GenericTypeValidator",
    "src.main.org.apache.commons.validator.GenericValidator": "src.main.org.apache.commons.validator.GenericValidator.GenericValidator",
    "src.main.org.apache.commons.validator.ISBNValidator": "src.main.org.apache.commons.validator.ISBNValidator.ISBNValidator",
    "src.main.org.apache.commons.validator.Msg": "src.main.org.apache.commons.validator.Msg.Msg",
    "src.main.org.apache.commons.validator.UrlValidator": "src.main.org.apache.commons.validator.UrlValidator.UrlValidator",
    "src.main.org.apache.commons.validator.Validator": "src.main.org.apache.commons.validator.Validator.Validator",
    "src.main.org.apache.commons.validator.ValidatorAction": "src.main.org.apache.commons.validator.ValidatorAction.ValidatorAction",
    "src.main.org.apache.commons.validator.ValidatorException": "src.main.org.apache.commons.validator.ValidatorException.ValidatorException",
    "src.main.org.apache.commons.validator.ValidatorResources": "src.main.org.apache.commons.validator.ValidatorResources.ValidatorResources",
    "src.main.org.apache.commons.validator.ValidatorResult": "src.main.org.apache.commons.validator.ValidatorResult.ValidatorResult",
    "src.main.org.apache.commons.validator.Var": "src.main.org.apache.commons.validator.Var.Var",

    "src.main.org.apache.commons.codec.binary.Base16": "src.main.org.apache.commons.codec.binary.Base16.Base16",
    "src.main.org.apache.commons.codec.binary.Base16InputStream": "src.main.org.apache.commons.codec.binary.Base16InputStream.Base16InputStream",
    "src.main.org.apache.commons.codec.binary.Base16OutputStream": "src.main.org.apache.commons.codec.binary.Base16OutputStream.Base16OutputStream",
    "src.main.org.apache.commons.codec.binary.Base32": "src.main.org.apache.commons.codec.binary.Base32.Base32",
    "src.main.org.apache.commons.codec.binary.Base32InputStream": "src.main.org.apache.commons.codec.binary.Base32InputStream.Base32InputStream",
    "src.main.org.apache.commons.codec.binary.Base32OutputStream": "src.main.org.apache.commons.codec.binary.Base32OutputStream.Base32OutputStream",
    "src.main.org.apache.commons.codec.binary.Base64": "src.main.org.apache.commons.codec.binary.Base64.Base64",
    "src.main.org.apache.commons.codec.binary.Base64InputStream": "src.main.org.apache.commons.codec.binary.Base64InputStream.Base64InputStream",
    "src.main.org.apache.commons.codec.binary.Base64OutputStream": "src.main.org.apache.commons.codec.binary.Base64OutputStream.Base64OutputStream",
    "src.main.org.apache.commons.codec.binary.BaseNCodec": "src.main.org.apache.commons.codec.binary.BaseNCodec.BaseNCodec",
    "src.main.org.apache.commons.codec.binary.BaseNCodecInputStream": "src.main.org.apache.commons.codec.binary.BaseNCodecInputStream.BaseNCodecInputStream",
    "src.main.org.apache.commons.codec.binary.BaseNCodecOutputStream": "src.main.org.apache.commons.codec.binary.BaseNCodecOutputStream.BaseNCodecOutputStream",
    "src.main.org.apache.commons.codec.binary.BinaryCodec": "src.main.org.apache.commons.codec.binary.BinaryCodec.BinaryCodec",
    "src.main.org.apache.commons.codec.binary.CharSequenceUtils": "src.main.org.apache.commons.codec.binary.CharSequenceUtils.CharSequenceUtils",
    "src.main.org.apache.commons.codec.binary.Hex": "src.main.org.apache.commons.codec.binary.Hex.Hex",
    "src.main.org.apache.commons.codec.binary.StringUtils": "src.main.org.apache.commons.codec.binary.StringUtils.StringUtils",
    "src.main.org.apache.commons.codec.cli.Digest": "src.main.org.apache.commons.codec.cli.Digest.Digest",
    "src.main.org.apache.commons.codec.digest.B64": "src.main.org.apache.commons.codec.digest.B64.B64",
    "src.main.org.apache.commons.codec.digest.Blake3": "src.main.org.apache.commons.codec.digest.Blake3.Blake3",
    "src.main.org.apache.commons.codec.digest.Blake3$Output": "src.main.org.apache.commons.codec.digest.Blake3.Output",
    "src.main.org.apache.commons.codec.digest.Blake3$ChunkState": "src.main.org.apache.commons.codec.digest.Blake3.ChunkState",
    "src.main.org.apache.commons.codec.digest.Blake3$EngineState": "src.main.org.apache.commons.codec.digest.Blake3.EngineState",
    "src.main.org.apache.commons.codec.digest.Crypt": "src.main.org.apache.commons.codec.digest.Crypt.Crypt",
    "src.main.org.apache.commons.codec.digest.HmacAlgorithms": "src.main.org.apache.commons.codec.digest.HmacAlgorithms.HmacAlgorithms",
    "src.main.org.apache.commons.codec.digest.HmacUtils": "src.main.org.apache.commons.codec.digest.HmacUtils.HmacUtils",
    "src.main.org.apache.commons.codec.digest.Md5Crypt": "src.main.org.apache.commons.codec.digest.Md5Crypt.Md5Crypt",
    "src.main.org.apache.commons.codec.digest.MessageDigestAlgorithms": "src.main.org.apache.commons.codec.digest.MessageDigestAlgorithms.MessageDigestAlgorithms",
    "src.main.org.apache.commons.codec.digest.MurmurHash2": "src.main.org.apache.commons.codec.digest.MurmurHash2.MurmurHash2",
    "src.main.org.apache.commons.codec.digest.MurmurHash3": "src.main.org.apache.commons.codec.digest.MurmurHash3.MurmurHash3",
    "src.main.org.apache.commons.codec.digest.MurmurHash3$IncrementalHash32x86": "src.main.org.apache.commons.codec.digest.MurmurHash3.IncrementalHash32x86",
    "src.main.org.apache.commons.codec.digest.MurmurHash3$IncrementalHash32": "src.main.org.apache.commons.codec.digest.MurmurHash3.IncrementalHash32",
    "src.main.org.apache.commons.codec.digest.PureJavaCrc32": "src.main.org.apache.commons.codec.digest.PureJavaCrc32.PureJavaCrc32",
    "src.main.org.apache.commons.codec.digest.PureJavaCrc32C": "src.main.org.apache.commons.codec.digest.PureJavaCrc32C.PureJavaCrc32C",
    "src.main.org.apache.commons.codec.digest.Sha2Crypt": "src.main.org.apache.commons.codec.digest.Sha2Crypt.Sha2Crypt",
    "src.main.org.apache.commons.codec.digest.UnixCrypt": "src.main.org.apache.commons.codec.digest.UnixCrypt.UnixCrypt",
    "src.main.org.apache.commons.codec.digest.XXHash32": "src.main.org.apache.commons.codec.digest.XXHash32.XXHash32",
    "src.main.org.apache.commons.codec.language.bm.BeiderMorseEncoder": "src.main.org.apache.commons.codec.language.bm.BeiderMorseEncoder.BeiderMorseEncoder",
    "src.main.org.apache.commons.codec.language.bm.Lang": "src.main.org.apache.commons.codec.language.bm.Lang.Lang",
    "src.main.org.apache.commons.codec.language.bm.Lang$LangRule": "src.main.org.apache.commons.codec.language.bm.Lang.LangRule",
    "src.main.org.apache.commons.codec.language.bm.Languages": "src.main.org.apache.commons.codec.language.bm.Languages.Languages",
    "src.main.org.apache.commons.codec.language.bm.Languages$LanguageSet": "src.main.org.apache.commons.codec.language.bm.Languages.LanguageSet",
    "src.main.org.apache.commons.codec.language.bm.Languages$AnyLanguage": "src.main.org.apache.commons.codec.language.bm.Languages.AnyLanguage",
    "src.main.org.apache.commons.codec.language.bm.Languages$NoLanguage": "src.main.org.apache.commons.codec.language.bm.Languages.NoLanguage",
    "src.main.org.apache.commons.codec.language.bm.Languages$SomeLanguages": "src.main.org.apache.commons.codec.language.bm.Languages.SomeLanguages",
    "src.main.org.apache.commons.codec.language.bm.NameType": "src.main.org.apache.commons.codec.language.bm.NameType.NameType",
    "src.main.org.apache.commons.codec.language.bm.PhoneticEngine": "src.main.org.apache.commons.codec.language.bm.PhoneticEngine.PhoneticEngine",
    "src.main.org.apache.commons.codec.language.bm.PhoneticEngine$PhonemeBuilder": "src.main.org.apache.commons.codec.language.bm.PhoneticEngine.PhonemeBuilder",
    "src.main.org.apache.commons.codec.language.bm.PhoneticEngine$RulesApplication": "src.main.org.apache.commons.codec.language.bm.PhoneticEngine.RulesApplication",
    "src.main.org.apache.commons.codec.language.bm.ResourceConstants": "src.main.org.apache.commons.codec.language.bm.ResourceConstants.ResourceConstants",
    "src.main.org.apache.commons.codec.language.bm.Rule": "src.main.org.apache.commons.codec.language.bm.Rule.Rule",
    "src.main.org.apache.commons.codec.language.bm.Rule$Phoneme": "src.main.org.apache.commons.codec.language.bm.Rule.Phoneme",
    "src.main.org.apache.commons.codec.language.bm.Rule$PhonemeExpr": "src.main.org.apache.commons.codec.language.bm.Rule.PhonemeExpr",
    "src.main.org.apache.commons.codec.language.bm.Rule$PhonemeList": "src.main.org.apache.commons.codec.language.bm.Rule.PhonemeList",
    "src.main.org.apache.commons.codec.language.bm.Rule$RPattern": "src.main.org.apache.commons.codec.language.bm.Rule.RPattern",
    "src.main.org.apache.commons.codec.language.bm.Rule1": "src.main.org.apache.commons.codec.language.bm.Rule1.Rule1",
    "src.main.org.apache.commons.codec.language.bm.RuleType": "src.main.org.apache.commons.codec.language.bm.RuleType.RuleType",
    "src.main.org.apache.commons.codec.language.AbstractCaverphone": "src.main.org.apache.commons.codec.language.AbstractCaverphone.AbstractCaverphone",
    "src.main.org.apache.commons.codec.language.Caverphone": "src.main.org.apache.commons.codec.language.Caverphone.Caverphone",
    "src.main.org.apache.commons.codec.language.Caverphone1": "src.main.org.apache.commons.codec.language.Caverphone1.Caverphone1",
    "src.main.org.apache.commons.codec.language.Caverphone2": "src.main.org.apache.commons.codec.language.Caverphone2.Caverphone2",
    "src.main.org.apache.commons.codec.language.ColognePhonetic": "src.main.org.apache.commons.codec.language.ColognePhonetic.ColognePhonetic",
    "src.main.org.apache.commons.codec.language.ColognePhonetic$CologneBuffer": "src.main.org.apache.commons.codec.language.ColognePhonetic.CologneBuffer",
    "src.main.org.apache.commons.codec.language.ColognePhonetic$CologneOutputBuffer": "src.main.org.apache.commons.codec.language.ColognePhonetic.CologneOutputBuffer",
    "src.main.org.apache.commons.codec.language.ColognePhonetic$CologneInputBuffer": "src.main.org.apache.commons.codec.language.ColognePhonetic.CologneInputBuffer",
    "src.main.org.apache.commons.codec.language.DaitchMokotoffSoundex": "src.main.org.apache.commons.codec.language.DaitchMokotoffSoundex.DaitchMokotoffSoundex",
    "src.main.org.apache.commons.codec.language.DaitchMokotoffSoundex$Branch": "src.main.org.apache.commons.codec.language.DaitchMokotoffSoundex.Branch",
    "src.main.org.apache.commons.codec.language.DaitchMokotoffSoundex$Rule": "src.main.org.apache.commons.codec.language.DaitchMokotoffSoundex.Rule",
    "src.main.org.apache.commons.codec.language.DoubleMetaPhone": "src.main.org.apache.commons.codec.language.DoubleMetaPhone.DoubleMetaPhone",
    "src.main.org.apache.commons.codec.language.DoubleMetaPhone$DoubleMetaphoneResult": "src.main.org.apache.commons.codec.language.DoubleMetaPhone.DoubleMetaphoneResult",
    "src.main.org.apache.commons.codec.language.MatchRatingApproachEncoder": "src.main.org.apache.commons.codec.language.MatchRatingApproachEncoder.MatchRatingApproachEncoder",
    "src.main.org.apache.commons.codec.language.Metaphone": "src.main.org.apache.commons.codec.language.Metaphone.Metaphone",
    "src.main.org.apache.commons.codec.language.Nysiis": "src.main.org.apache.commons.codec.language.Nysiis.Nysiis",
    "src.main.org.apache.commons.codec.language.RefinedSoundex": "src.main.org.apache.commons.codec.language.RefinedSoundex.RefinedSoundex",
    "src.main.org.apache.commons.codec.language.Soundex": "src.main.org.apache.commons.codec.language.Soundex.Soundex",
    "src.main.org.apache.commons.codec.language.SoundexUtils": "src.main.org.apache.commons.codec.language.SoundexUtils.SoundexUtils",
    "src.main.org.apache.commons.codec.net.BCodec": "src.main.org.apache.commons.codec.net.BCodec.BCodec",
    "src.main.org.apache.commons.codec.net.PercentCodec": "src.main.org.apache.commons.codec.net.PercentCodec.PercentCodec",
    "src.main.org.apache.commons.codec.net.QCodec": "src.main.org.apache.commons.codec.net.QCodec.QCodec",
    "src.main.org.apache.commons.codec.net.QuotedPrintableCodec": "src.main.org.apache.commons.codec.net.QuotedPrintableCodec.QuotedPrintableCodec",
    "src.main.org.apache.commons.codec.net.RFC1522Codec": "src.main.org.apache.commons.codec.net.RFC1522Codec.RFC1522Codec",
    "src.main.org.apache.commons.codec.net.URLCodec": "src.main.org.apache.commons.codec.net.URLCodec.URLCodec",
    "src.main.org.apache.commons.codec.net.Utils": "src.main.org.apache.commons.codec.net.Utils.Utils",
    "src.main.org.apache.commons.codec.BinaryDecoder": "src.main.org.apache.commons.codec.BinaryDecoder.BinaryDecoder",
    "src.main.org.apache.commons.codec.BinaryEncoder": "src.main.org.apache.commons.codec.BinaryEncoder.BinaryEncoder",
    "src.main.org.apache.commons.codec.CharEncoding": "src.main.org.apache.commons.codec.CharEncoding.CharEncoding",
    "src.main.org.apache.commons.codec.Charsets": "src.main.org.apache.commons.codec.Charsets.Charsets",
    "src.main.org.apache.commons.codec.CodecPolicy": "src.main.org.apache.commons.codec.CodecPolicy.CodecPolicy",
    "src.main.org.apache.commons.codec.Decoder": "src.main.org.apache.commons.codec.Decoder.Decoder",
    "src.main.org.apache.commons.codec.DecoderException": "src.main.org.apache.commons.codec.DecoderException.DecoderException",
    "src.main.org.apache.commons.codec.Encoder": "src.main.org.apache.commons.codec.Encoder.Encoder",
    "src.main.org.apache.commons.codec.EncoderException": "src.main.org.apache.commons.codec.EncoderException.EncoderException",
    "src.main.org.apache.commons.codec.Resources": "src.main.org.apache.commons.codec.Resources.Resources",
    "src.main.org.apache.commons.codec.StringDecoder": "src.main.org.apache.commons.codec.StringDecoder.StringDecoder",
    "src.main.org.apache.commons.codec.StringEncoder": "src.main.org.apache.commons.codec.StringEncoder.StringEncoder",
    "src.main.org.apache.commons.codec.StringEncoderComparator": "src.main.org.apache.commons.codec.StringEncoderComparator.StringEncoderComparator",
    "src.test.org.apache.commons.codec.net.RFC1522CodecTest$RFC1522TestCodec": "src.test.org.apache.commons.codec.net.RFC1522CodecTest.RFC1522TestCodec",
    "src.test.org.apache.commons.codec.digest.PureJavaCrc32Test$Table": "src.test.org.apache.commons.codec.digest.PureJavaCrc32Test.Table",
    "src.test.org.apache.commons.codec.digest.PureJavaCrc32Test$PerformanceTest": "src.test.org.apache.commons.codec.digest.PureJavaCrc32Test.PerformanceTest",
    "src.test.org.apache.commons.codec.binary.Base16TestData": "src.test.org.apache.commons.codec.binary.Base16TestData.Base16TestData",
    "src.test.org.apache.commons.codec.binary.Base32TestData": "src.test.org.apache.commons.codec.binary.Base32TestData.Base32TestData",
    "src.test.org.apache.commons.codec.binary.Base64TestData": "src.test.org.apache.commons.codec.binary.Base64TestData.Base64TestData",
    "src.test.org.apache.commons.codec.binary.BaseNTestData": "src.test.org.apache.commons.codec.binary.BaseNTestData.BaseNTestData",
    "src.test.org.apache.commons.codec.binary.Codec105ErrorInputStream": "src.test.org.apache.commons.codec.binary.Codec105ErrorInputStream.Codec105ErrorInputStream",
    
    "java.util.concurrent.TimeUnit": "datetime.timedelta",
    "java.time.temporal.ChronoUnit": "datetime.timedelta",
    "java.time.Duration": "datetime.timedelta",
    "src.main.org.apache.commons.pool2.impl.AbandonedConfig": "src.main.org.apache.commons.pool2.impl.AbandonedConfig.AbandonedConfig",
    "src.main.org.apache.commons.pool2.impl.BaseGenericObjectPool": "src.main.org.apache.commons.pool2.impl.BaseGenericObjectPool.BaseGenericObjectPool",
    "src.main.org.apache.commons.pool2.impl.BaseGenericObjectPool$EvictionIterator": "src.main.org.apache.commons.pool2.impl.BaseGenericObjectPool.EvictionIterator",
    "src.main.org.apache.commons.pool2.impl.BaseGenericObjectPool$Evictor": "src.main.org.apache.commons.pool2.impl.BaseGenericObjectPool.Evictor",
    "src.main.org.apache.commons.pool2.impl.BaseGenericObjectPool$IdentityWrapper": "src.main.org.apache.commons.pool2.impl.BaseGenericObjectPool.IdentityWrapper",
    "src.main.org.apache.commons.pool2.impl.BaseGenericObjectPool$StatsStore": "src.main.org.apache.commons.pool2.impl.BaseGenericObjectPool.StatsStore",
    "src.main.org.apache.commons.pool2.impl.BaseObjectPoolConfig": "src.main.org.apache.commons.pool2.impl.BaseObjectPoolConfig.BaseObjectPoolConfig",
    "src.main.org.apache.commons.pool2.impl.CallStack": "src.main.org.apache.commons.pool2.impl.CallStack.CallStack",
    "src.main.org.apache.commons.pool2.impl.CallStackUtils": "src.main.org.apache.commons.pool2.impl.CallStackUtils.CallStackUtils",
    "src.main.org.apache.commons.pool2.impl.DefaultEvictionPolicy": "src.main.org.apache.commons.pool2.impl.DefaultEvictionPolicy.DefaultEvictionPolicy",
    "src.main.org.apache.commons.pool2.impl.DefaultPooledObject": "src.main.org.apache.commons.pool2.impl.DefaultPooledObject.DefaultPooledObject",
    "src.main.org.apache.commons.pool2.impl.DefaultPooledObjectInfo": "src.main.org.apache.commons.pool2.impl.DefaultPooledObjectInfo.DefaultPooledObjectInfo",
    "src.main.org.apache.commons.pool2.impl.DefaultPooledObjectInfoMBean": "src.main.org.apache.commons.pool2.impl.DefaultPooledObjectInfoMBean.DefaultPooledObjectInfoMBean",
    "src.main.org.apache.commons.pool2.impl.EvictionConfig": "src.main.org.apache.commons.pool2.impl.EvictionConfig.EvictionConfig",
    "src.main.org.apache.commons.pool2.impl.EvictionPolicy": "src.main.org.apache.commons.pool2.impl.EvictionPolicy.EvictionPolicy",
    "src.main.org.apache.commons.pool2.impl.EvictionTimer": "src.main.org.apache.commons.pool2.impl.EvictionTimer.EvictionTimer",
    "src.main.org.apache.commons.pool2.impl.EvictionTimer$Reaper": "src.main.org.apache.commons.pool2.impl.EvictionTimer.EvictionTimer.Reaper",
    "src.main.org.apache.commons.pool2.impl.EvictionTimer$WeakRunner": "src.main.org.apache.commons.pool2.impl.EvictionTimer.EvictionTimer.WeakRunner",
    "src.main.org.apache.commons.pool2.impl.GenericKeyedObjectPoolConfig": "src.main.org.apache.commons.pool2.impl.GenericKeyedObjectPoolConfig.GenericKeyedObjectPoolConfig",
    "src.main.org.apache.commons.pool2.impl.GenericKeyedObjectPoolMXBean": "src.main.org.apache.commons.pool2.impl.GenericKeyedObjectPoolMXBean.GenericKeyedObjectPoolMXBean",
    "src.main.org.apache.commons.pool2.impl.GenericObjectPoolConfig": "src.main.org.apache.commons.pool2.impl.GenericObjectPoolConfig.GenericObjectPoolConfig",
    "src.main.org.apache.commons.pool2.impl.GenericObjectPoolMXBean": "src.main.org.apache.commons.pool2.impl.GenericObjectPoolMXBean.GenericObjectPoolMXBean",
    "src.main.org.apache.commons.pool2.impl.InterruptibleReentrantLock": "src.main.org.apache.commons.pool2.impl.InterruptibleReentrantLock.InterruptibleReentrantLock",
    "src.main.org.apache.commons.pool2.impl.LinkedBlockingDeque": "src.main.org.apache.commons.pool2.impl.LinkedBlockingDeque.LinkedBlockingDeque",
    "src.main.org.apache.commons.pool2.impl.LinkedBlockingDeque$AbstractItr": "src.main.org.apache.commons.pool2.impl.LinkedBlockingDeque.AbstractItr",
    "src.main.org.apache.commons.pool2.impl.LinkedBlockingDeque$DescendingItr": "src.main.org.apache.commons.pool2.impl.LinkedBlockingDeque.DescendingItr",
    "src.main.org.apache.commons.pool2.impl.LinkedBlockingDeque$Itr": "src.main.org.apache.commons.pool2.impl.LinkedBlockingDeque.Itr",
    "src.main.org.apache.commons.pool2.impl.LinkedBlockingDeque$Node": "src.main.org.apache.commons.pool2.impl.LinkedBlockingDeque.Node",
    "src.main.org.apache.commons.pool2.impl.NoOpCallStack": "src.main.org.apache.commons.pool2.impl.NoOpCallStack.NoOpCallStack",
    "src.main.org.apache.commons.pool2.impl.PoolImplUtils": "src.main.org.apache.commons.pool2.impl.PoolImplUtils.PoolImplUtils",
    "src.main.org.apache.commons.pool2.impl.PooledSoftReference": "src.main.org.apache.commons.pool2.impl.PooledSoftReference.PooledSoftReference",
    "src.main.org.apache.commons.pool2.impl.SecurityManagerCallStack": "src.main.org.apache.commons.pool2.impl.SecurityManagerCallStack.SecurityManagerCallStack",
    "src.main.org.apache.commons.pool2.impl.SecurityManagerCallStack$PrivateSecurityManager": "src.main.org.apache.commons.pool2.impl.SecurityManagerCallStack.PrivateSecurityManager",
    "src.main.org.apache.commons.pool2.impl.SecurityManagerCallStack$Snapshot": "src.main.org.apache.commons.pool2.impl.SecurityManagerCallStack.Snapshot",
    "src.main.org.apache.commons.pool2.impl.ThrowableCallStack": "src.main.org.apache.commons.pool2.impl.ThrowableCallStack.ThrowableCallStack",
    "src.main.org.apache.commons.pool2.impl.ThrowableCallStack$Snapshot": "src.main.org.apache.commons.pool2.impl.ThrowableCallStack.Snapshot",
    "src.main.org.apache.commons.pool2.proxy.BaseProxyHandler": "src.main.org.apache.commons.pool2.proxy.BaseProxyHandler.BaseProxyHandler",
    "src.main.org.apache.commons.pool2.proxy.CglibProxySource": "src.main.org.apache.commons.pool2.proxy.CglibProxySource.CglibProxySource",
    "src.main.org.apache.commons.pool2.proxy.JdkProxyHandler": "src.main.org.apache.commons.pool2.proxy.JdkProxyHandler.JdkProxyHandler",
    "src.main.org.apache.commons.pool2.proxy.JdkProxySource": "src.main.org.apache.commons.pool2.proxy.JdkProxySource.JdkProxySource",
    "src.main.org.apache.commons.pool2.proxy.ProxiedKeyedObjectPool": "src.main.org.apache.commons.pool2.proxy.ProxiedKeyedObjectPool.ProxiedKeyedObjectPool",
    "src.main.org.apache.commons.pool2.proxy.ProxiedObjectPool": "src.main.org.apache.commons.pool2.proxy.ProxiedObjectPool.ProxiedObjectPool",
    "src.main.org.apache.commons.pool2.proxy.ProxySource": "src.main.org.apache.commons.pool2.proxy.ProxySource.ProxySource",
    "src.main.org.apache.commons.pool2.BaseKeyedPooledObjectFactory": "src.main.org.apache.commons.pool2.BaseKeyedPooledObjectFactory.BaseKeyedPooledObjectFactory",
    "src.main.org.apache.commons.pool2.BaseObject": "src.main.org.apache.commons.pool2.BaseObject.BaseObject",
    "src.main.org.apache.commons.pool2.BaseObjectPool": "src.main.org.apache.commons.pool2.BaseObjectPool.BaseObjectPool",
    "src.main.org.apache.commons.pool2.BasePooledObjectFactory": "src.main.org.apache.commons.pool2.BasePooledObjectFactory.BasePooledObjectFactory",
    "src.main.org.apache.commons.pool2.DestroyMode": "src.main.org.apache.commons.pool2.DestroyMode.DestroyMode",
    "src.main.org.apache.commons.pool2.KeyedObjectPool": "src.main.org.apache.commons.pool2.KeyedObjectPool.KeyedObjectPool",
    "src.main.org.apache.commons.pool2.KeyedPooledObjectFactory": "src.main.org.apache.commons.pool2.KeyedPooledObjectFactory.KeyedPooledObjectFactory",
    "src.main.org.apache.commons.pool2.ObjectPool": "src.main.org.apache.commons.pool2.ObjectPool.ObjectPool",
    "src.main.org.apache.commons.pool2.PoolUtils": "src.main.org.apache.commons.pool2.PoolUtils.PoolUtils",
    "src.main.org.apache.commons.pool2.PoolUtils$ErodingFactor": "src.main.org.apache.commons.pool2.PoolUtils.ErodingFactor",
    "src.main.org.apache.commons.pool2.PoolUtils$ErodingKeyedObjectPool": "src.main.org.apache.commons.pool2.PoolUtils.ErodingKeyedObjectPool",
    "src.main.org.apache.commons.pool2.PooledObject": "src.main.org.apache.commons.pool2.PooledObject.PooledObject",
    "src.main.org.apache.commons.pool2.PooledObjectFactory": "src.main.org.apache.commons.pool2.PooledObjectFactory.PooledObjectFactory",
    "src.main.org.apache.commons.pool2.PooledObjectState": "src.main.org.apache.commons.pool2.PooledObjectState.PooledObjectState",
    "src.main.org.apache.commons.pool2.SwallowedExceptionListener": "src.main.org.apache.commons.pool2.SwallowedExceptionListener.SwallowedExceptionListener",
    "src.main.org.apache.commons.pool2.TrackedUse": "src.main.org.apache.commons.pool2.TrackedUse.TrackedUse",
    "src.main.org.apache.commons.pool2.UsageTracking": "src.main.org.apache.commons.pool2.UsageTracking.UsageTracking",
    "src.test.org.apache.commons.pool2.impl.TestConstants": "src.test.org.apache.commons.pool2.impl.TestConstants.TestConstants",
    "src.test.org.apache.commons.pool2.impl.TestPoolImplUtils$FactoryAB": "src.test.org.apache.commons.pool2.impl.TestPoolImplUtils.FactoryAB",
    "src.test.org.apache.commons.pool2.impl.TestPoolImplUtils$FactoryBA": "src.test.org.apache.commons.pool2.impl.TestPoolImplUtils.FactoryBA",
    "src.test.org.apache.commons.pool2.impl.TestPoolImplUtils$FactoryC": "src.test.org.apache.commons.pool2.impl.TestPoolImplUtils.FactoryC",
    "src.test.org.apache.commons.pool2.impl.TestPoolImplUtils$FactoryDE": "src.test.org.apache.commons.pool2.impl.TestPoolImplUtils.FactoryDE",
    "src.test.org.apache.commons.pool2.impl.TestPoolImplUtils$FactoryF": "src.test.org.apache.commons.pool2.impl.TestPoolImplUtils.FactoryF",
    "src.test.org.apache.commons.pool2.impl.TestPoolImplUtils$NotSimpleFactory": "src.test.org.apache.commons.pool2.impl.TestPoolImplUtils.NotSimpleFactory",
    "src.test.org.apache.commons.pool2.impl.TestPoolImplUtils$SimpleFactory": "src.test.org.apache.commons.pool2.impl.TestPoolImplUtils.SimpleFactory",
    "src.test.org.apache.commons.pool2.performance.SleepingObjectFactory": "src.test.org.apache.commons.pool2.performance.SleepingObjectFactory.SleepingObjectFactory",
    "src.test.org.apache.commons.pool2.proxy.BaseTestProxiedKeyedObjectPool$TestObject": "src.test.org.apache.commons.pool2.proxy.BaseTestProxiedKeyedObjectPool.TestObject",
    "src.test.org.apache.commons.pool2.proxy.BaseTestProxiedKeyedObjectPool$TestObjectImpl": "src.test.org.apache.commons.pool2.proxy.BaseTestProxiedKeyedObjectPool.TestObjectImpl",
    "src.test.org.apache.commons.pool2.proxy.BaseTestProxiedObjectPool.java$TestObject": "src.test.org.apache.commons.pool2.proxy.BaseTestProxiedObjectPool.java.TestObject",
    "src.test.org.apache.commons.pool2.proxy.BaseTestProxiedObjectPool.java$TestObjectImpl": "src.test.org.apache.commons.pool2.proxy.BaseTestProxiedObjectPool.java.TestObjectImpl",
    "src.test.org.apache.commons.pool2.MethodCall": "src.test.org.apache.commons.pool2.MethodCall.MethodCall",
    "src.test.org.apache.commons.pool2.MethodCallPoolableObjectFactory": "src.test.org.apache.commons.pool2.MethodCallPoolableObjectFactory.MethodCallPoolableObjectFactory",
    "src.test.org.apache.commons.pool2.PrivateException": "src.test.org.apache.commons.pool2.PrivateException.PrivateException",
    "src.test.org.apache.commons.pool2.TestBaseObjectPool$TestObjectPool": "src.test.org.apache.commons.pool2.TestBaseObjectPool.TestObjectPool",
    "src.test.org.apache.commons.pool2.TestKeyedObjectPool$FailingKeyedPooledObjectFactory": "src.test.org.apache.commons.pool2.TestKeyedObjectPool.FailingKeyedPooledObjectFactory",
    "src.test.org.apache.commons.pool2.TestPoolUtils": "src.test.org.apache.commons.pool2.TestPoolUtils.TestPoolUtils",
    "src.test.org.apache.commons.pool2.TestPoolUtils$MethodCallLogger": "src.test.org.apache.commons.pool2.TestPoolUtils.MethodCallLogger",
    "src.test.org.apache.commons.pool2.TestTrackedUse$DefaultTrackedUse": "src.test.org.apache.commons.pool2.TestTrackedUse.DefaultTrackedUse",
    "src.test.org.apache.commons.pool2.VisitTracker": "src.test.org.apache.commons.pool2.VisitTracker.VisitTracker",
    "src.test.org.apache.commons.pool2.VisitTrackerFactory": "src.test.org.apache.commons.pool2.VisitTrackerFactory.VisitTrackerFactory",
    "src.test.org.apache.commons.pool2.Waiter": "src.test.org.apache.commons.pool2.Waiter.Waiter",
    "src.test.org.apache.commons.pool2.WaiterFactory": "src.test.org.apache.commons.pool2.WaiterFactory.WaiterFactory",
    "src.test.org.apache.commons.pool2.impl.ConstantsTest": "src.test.org.apache.commons.pool2.impl.TestConstants.TestConstants",
    "src.test.org.apache.commons.pool2.impl.PoolImplUtilsTest$FactoryAB": "src.test.org.apache.commons.pool2.impl.TestPoolImplUtils.FactoryAB",
    "src.test.org.apache.commons.pool2.impl.PoolImplUtilsTest$FactoryBA": "src.test.org.apache.commons.pool2.impl.TestPoolImplUtils.FactoryBA",
    "src.test.org.apache.commons.pool2.impl.PoolImplUtilsTest$FactoryC": "src.test.org.apache.commons.pool2.impl.TestPoolImplUtils.FactoryC",
    "src.test.org.apache.commons.pool2.impl.PoolImplUtilsTest$FactoryDE": "src.test.org.apache.commons.pool2.impl.TestPoolImplUtils.FactoryDE",
    "src.test.org.apache.commons.pool2.impl.PoolImplUtilsTest$FactoryF": "src.test.org.apache.commons.pool2.impl.TestPoolImplUtils.FactoryF",
    "src.test.org.apache.commons.pool2.impl.PoolImplUtilsTest$NotSimpleFactory": "src.test.org.apache.commons.pool2.impl.TestPoolImplUtils.NotSimpleFactory",
    "src.test.org.apache.commons.pool2.impl.PoolImplUtilsTest$SimpleFactory": "src.test.org.apache.commons.pool2.impl.TestPoolImplUtils.SimpleFactory",
    "src.test.org.apache.commons.pool2.BaseObjectPoolTest$TestObjectPool": "src.test.org.apache.commons.pool2.TestBaseObjectPool.TestObjectPool",
    "src.test.org.apache.commons.pool2.KeyedObjectPoolTest$FailingKeyedPooledObjectFactory": "src.test.org.apache.commons.pool2.TestKeyedObjectPool.FailingKeyedPooledObjectFactory",
    "src.test.org.apache.commons.pool2.PoolUtilsTest": "src.test.org.apache.commons.pool2.TestPoolUtils.TestPoolUtils",
    "src.test.org.apache.commons.pool2.PoolUtilsTest$MethodCallLogger": "src.test.org.apache.commons.pool2.TestPoolUtils.MethodCallLogger",
    "src.test.org.apache.commons.pool2.TrackedUseTest$DefaultTrackedUse": "src.test.org.apache.commons.pool2.TestTrackedUse.DefaultTrackedUse",
    
    "src.main.com.kamikaze.pfordelta.LCPForDelta": "src.main.com.kamikaze.pfordelta.LCPForDelta.LCPForDelta",
    "src.main.com.kamikaze.pfordelta.PForDelta": "src.main.com.kamikaze.pfordelta.PForDelta.PForDelta",
    "src.main.com.kamikaze.pfordelta.PForDeltaUnpack128": "src.main.com.kamikaze.pfordelta.PForDeltaUnpack128.PForDeltaUnpack128",
    "src.main.com.kamikaze.pfordelta.PForDeltaUnpack128WIthIntBuffer": "src.main.com.kamikaze.pfordelta.PForDeltaUnpack128WIthIntBuffer.PForDeltaUnpack128WIthIntBuffer",
    "src.main.com.kamikaze.pfordelta.Simple16": "src.main.com.kamikaze.pfordelta.Simple16.Simple16",
    "src.main.com.kamikaze.pfordelta.Simple16WithHardCodes": "src.main.com.kamikaze.pfordelta.Simple16WithHardCodes.Simple16WithHardCodes",
    "src.main.me.lemire.integercompression.benchmarktools.Benchmark": "src.main.me.lemire.integercompression.benchmarktools.Benchmark.Benchmark",
    "src.main.me.lemire.integercompression.benchmarktools.BenchmarkBitPacking": "src.main.me.lemire.integercompression.benchmarktools.BenchmarkBitPacking.BenchmarkBitPacking",
    "src.main.me.lemire.integercompression.benchmarktools.BenchmarkCSV": "src.main.me.lemire.integercompression.benchmarktools.BenchmarkCSV.BenchmarkCSV",
    "src.main.me.lemire.integercompression.benchmarktools.BenchmarkOffsettedSeries": "src.main.me.lemire.integercompression.benchmarktools.BenchmarkOffsettedSeries.BenchmarkOffsettedSeries",
    "src.main.me.lemire.integercompression.benchmarktools.BenchmarkSkippable": "src.main.me.lemire.integercompression.benchmarktools.BenchmarkSkippable.BenchmarkSkippable",
    "src.main.me.lemire.integercompression.benchmarktools.PerformanceLogger": "src.main.me.lemire.integercompression.benchmarktools.PerformanceLogger.PerformanceLogger",
    "src.main.me.lemire.integercompression.benchmarktools.PerformanceLogger$Timer": "src.main.me.lemire.integercompression.benchmarktools.PerformanceLogger$Timer",
    "src.main.me.lemire.integercompression.differential.Delta": "src.main.me.lemire.integercompression.differential.Delta.Delta",
    "src.main.me.lemire.integercompression.differential.IntegratedBinaryPacking": "src.main.me.lemire.integercompression.differential.IntegratedBinaryPacking.IntegratedBinaryPacking",
    "src.main.me.lemire.integercompression.differential.IntegratedBitPacking": "src.main.me.lemire.integercompression.differential.IntegratedBitPacking.IntegratedBitPacking",
    "src.main.me.lemire.integercompression.differential.IntegratedByteIntegerCODEC": "src.main.me.lemire.integercompression.differential.IntegratedByteIntegerCODEC.IntegratedByteIntegerCODEC",
    "src.main.me.lemire.integercompression.differential.IntegratedComposition": "src.main.me.lemire.integercompression.differential.IntegratedComposition.IntegratedComposition",
    "src.main.me.lemire.integercompression.differential.IntegratedIntCompressor": "src.main.me.lemire.integercompression.differential.IntegratedIntCompressor.IntegratedIntCompressor",
    "src.main.me.lemire.integercompression.differential.IntegratedIntegerCODEC": "src.main.me.lemire.integercompression.differential.IntegratedIntegerCODEC.IntegratedIntegerCODEC",
    "src.main.me.lemire.integercompression.differential.IntegratedVariableByte": "src.main.me.lemire.integercompression.differential.IntegratedVariableByte.IntegratedVariableByte",
    "src.main.me.lemire.integercompression.differential.SkippableIntegratedComposition": "src.main.me.lemire.integercompression.differential.SkippableIntegratedComposition.SkippableIntegratedComposition",
    "src.main.me.lemire.integercompression.differential.SkippableIntegratedIntegerCODEC": "src.main.me.lemire.integercompression.differential.SkippableIntegratedIntegerCODEC.SkippableIntegratedIntegerCODEC",
    "src.main.me.lemire.integercompression.differential.XorBinaryPacking": "src.main.me.lemire.integercompression.differential.XorBinaryPacking.XorBinaryPacking",
    "src.main.me.lemire.integercompression.synth.ClusteredDataGenerator": "src.main.me.lemire.integercompression.synth.ClusteredDataGenerator.ClusteredDataGenerator",
    "src.main.me.lemire.integercompression.synth.UniformDataGenerator": "src.main.me.lemire.integercompression.synth.UniformDataGenerator.UniformDataGenerator",
    "src.main.me.lemire.integercompression.synth.ClusteredDataGenerator": "src.main.me.lemire.integercompression.synth.ClusteredDataGenerator.ClusteredDataGenerator",
    "src.main.me.lemire.integercompression.vector.VectorBitPacker": "src.main.me.lemire.integercompression.vector.VectorBitPacker.VectorBitPacker",
    "src.main.me.lemire.integercompression.vector.VectorBitPackerTerse": "src.main.me.lemire.integercompression.vector.VectorBitPackerTerse.VectorBitPackerTerse",
    "src.main.me.lemire.integercompression.vector.VectorFastPFOR": "src.main.me.lemire.integercompression.vector.VectorFastPFOR.VectorFastPFOR",
    "src.main.me.lemire.integercompression.BinaryPacking": "src.main.me.lemire.integercompression.BinaryPacking.BinaryPacking",
    "src.main.me.lemire.integercompression.BitPacking": "src.main.me.lemire.integercompression.BitPacking.BitPacking",
    "src.main.me.lemire.integercompression.ByteIntegerCODEC": "src.main.me.lemire.integercompression.ByteIntegerCODEC.ByteIntegerCODEC",
    "src.main.me.lemire.integercompression.Composition": "src.main.me.lemire.integercompression.Composition.Composition",
    "src.main.me.lemire.integercompression.DeltaZigzagBinaryPacking": "src.main.me.lemire.integercompression.DeltaZigzagBinaryPacking.DeltaZigzagBinaryPacking",
    "src.main.me.lemire.integercompression.DeltaZigzagEncoding": "src.main.me.lemire.integercompression.DeltaZigzagEncoding.DeltaZigzagEncoding",
    "src.main.me.lemire.integercompression.DeltaZigzagEncoding$Context": "src.main.me.lemire.integercompression.DeltaZigzagEncoding.Context",
    "src.main.me.lemire.integercompression.DeltaZigzagEncoding$Encoder": "src.main.me.lemire.integercompression.DeltaZigzagEncoding.Encoder",
    "src.main.me.lemire.integercompression.DeltaZigzagEncoding$Decoder": "src.main.me.lemire.integercompression.DeltaZigzagEncoding.Decoder",
    "src.main.me.lemire.integercompression.DeltaZigzagVariableByte": "src.main.me.lemire.integercompression.DeltaZigzagVariableByte.DeltaZigzagVariableByte",
    "src.main.me.lemire.integercompression.FastPFOR": "src.main.me.lemire.integercompression.FastPFOR.FastPFOR",
    "src.main.me.lemire.integercompression.FastPFOR128": "src.main.me.lemire.integercompression.FastPFOR128.FastPFOR128",
    "src.main.me.lemire.integercompression.GroupSimple9": "src.main.me.lemire.integercompression.GroupSimple9.GroupSimple9",
    "src.main.me.lemire.integercompression.IntCompressor": "src.main.me.lemire.integercompression.IntCompressor.IntCompressor",
    "src.main.me.lemire.integercompression.IntWrapper": "src.main.me.lemire.integercompression.IntWrapper.IntWrapper",
    "src.main.me.lemire.integercompression.IntegerCODEC": "src.main.me.lemire.integercompression.IntegerCODEC.IntegerCODEC",
    "src.main.me.lemire.integercompression.JustCopy": "src.main.me.lemire.integercompression.JustCopy.JustCopy",
    "src.main.me.lemire.integercompression.Kamikaze": "src.main.me.lemire.integercompression.Kamikaze.Kamikaze",
    "src.main.me.lemire.integercompression.NewPFD": "src.main.me.lemire.integercompression.NewPFD.NewPFD",
    "src.main.me.lemire.integercompression.NewPFDS16": "src.main.me.lemire.integercompression.NewPFDS16.NewPFDS16",
    "src.main.me.lemire.integercompression.NewPFDS9": "src.main.me.lemire.integercompression.NewPFDS9.NewPFDS9",
    "src.main.me.lemire.integercompression.OptPFD": "src.main.me.lemire.integercompression.OptPFD.OptPFD",
    "src.main.me.lemire.integercompression.OptPFDS16": "src.main.me.lemire.integercompression.OptPFDS16.OptPFDS16",
    "src.main.me.lemire.integercompression.OptPFDS9": "src.main.me.lemire.integercompression.OptPFDS9.OptPFDS9",
    "src.main.me.lemire.integercompression.S16": "src.main.me.lemire.integercompression.S16.S16",
    "src.main.me.lemire.integercompression.S9": "src.main.me.lemire.integercompression.S9.S9",
    "src.main.me.lemire.integercompression.Simple16": "src.main.me.lemire.integercompression.Simple16.Simple16",
    "src.main.me.lemire.integercompression.Simple9": "src.main.me.lemire.integercompression.Simple9.Simple9",
    "src.main.me.lemire.integercompression.SkippableComposition": "src.main.me.lemire.integercompression.SkippableComposition.SkippableComposition",
    "src.main.me.lemire.integercompression.SkippableIntegerCODEC": "src.main.me.lemire.integercompression.SkippableIntegerCODEC.SkippableIntegerCODEC",
    "src.main.me.lemire.integercompression.UncompressibleInputException": "src.main.me.lemire.integercompression.UncompressibleInputException.UncompressibleInputException",
    "src.main.me.lemire.integercompression.Util": "src.main.me.lemire.integercompression.Util.Util",
    "src.main.me.lemire.integercompression.VariableByte": "src.main.me.lemire.integercompression.VariableByte.VariableByte",
    "src.main.me.lemire.longcompression.differential.LongDelta": "src.main.me.lemire.longcompression.differential.LongDelta.LongDelta",
    "src.main.me.lemire.longcompression.ByteLongCODEC": "src.main.me.lemire.longcompression.ByteLongCODEC.ByteLongCODEC",
    "src.main.me.lemire.longcompression.IntegratedLongCODEC": "src.main.me.lemire.longcompression.IntegratedLongCODEC.IntegratedLongCODEC",
    "src.main.me.lemire.longcompression.LongAs2IntsCodec": "src.main.me.lemire.longcompression.LongAs2IntsCodec.LongAs2IntsCodec",
    "src.main.me.lemire.longcompression.LongCODEC": "src.main.me.lemire.longcompression.LongCODEC.LongCODEC",
    "src.main.me.lemire.longcompression.LongComposition": "src.main.me.lemire.longcompression.LongComposition.LongComposition",
    "src.main.me.lemire.longcompression.LongJustCopy": "src.main.me.lemire.longcompression.LongJustCopy.LongJustCopy",
    "src.main.me.lemire.longcompression.LongUtil": "src.main.me.lemire.longcompression.LongUtil.LongUtil",
    "src.main.me.lemire.longcompression.LongVariableByte": "src.main.me.lemire.longcompression.LongVariableByte.LongVariableByte",
    "src.main.me.lemire.longcompression.RoaringIntPacking": "src.main.me.lemire.longcompression.RoaringIntPacking.RoaringIntPacking",
    "src.main.me.lemire.longcompression.SkippableLongCODEC": "src.main.me.lemire.longcompression.SkippableLongCODEC.SkippableLongCODEC",
    "src.main.me.lemire.longcompression.SkippableLongComposition": "src.main.me.lemire.longcompression.SkippableLongComposition.SkippableLongComposition",
    "src.test.me.lemire.integercompression.DeltaZigzagEncodingTest$SpotChecker": "src.test.me.lemire.integercompression.DeltaZigzagEncodingTest.SpotChecker",
    "src.test.me.lemire.integercompression.TestUtils": "src.test.me.lemire.integercompression.TestUtils.TestUtils",
    "src.test.me.lemire.integercompression.UtilsTest": "src.test.me.lemire.integercompression.TestUtils.UtilsTest",
    "src.test.me.lemire.longcompression.synth.LongClusteredDataGenerator": "src.test.me.lemire.longcompression.synth.LongClusteredDataGenerator.LongClusteredDataGenerator",
    "src.test.me.lemire.longcompression.synth.LongUniformDataGenerator": "src.test.me.lemire.longcompression.synth.LongUniformDataGenerator.LongUniformDataGenerator",
    "src.test.me.lemire.longcompression.LongTestUtils": "src.test.me.lemire.longcompression.LongTestUtils.LongTestUtils",

    "src.main.org.apache.commons.exec.environment.DefaultProcessingEnvironment": "src.main.org.apache.commons.exec.environment.DefaultProcessingEnvironment.DefaultProcessingEnvironment",
    "src.main.org.apache.commons.exec.environment.EnvironmentUtils": "src.main.org.apache.commons.exec.environment.EnvironmentUtils.EnvironmentUtils",
    "src.main.org.apache.commons.exec.environment.EnvironmentUtils": "src.main.org.apache.commons.exec.environment.EnvironmentUtils.EnvironmentUtils",
    "src.main.org.apache.commons.exec.environment.OpenVmsProcessingEnvironment": "src.main.org.apache.commons.exec.environment.OpenVmsProcessingEnvironment.OpenVmsProcessingEnvironment",
    "src.main.org.apache.commons.exec.launcher.CommandLauncher": "src.main.org.apache.commons.exec.launcher.CommandLauncher.CommandLauncher",
    "src.main.org.apache.commons.exec.launcher.CommandLauncherFactory": "src.main.org.apache.commons.exec.launcher.CommandLauncherFactory.CommandLauncherFactory",
    "src.main.org.apache.commons.exec.launcher.CommandLauncherImpl": "src.main.org.apache.commons.exec.launcher.CommandLauncherImpl.CommandLauncherImpl",
    "src.main.org.apache.commons.exec.launcher.CommandLauncherProxy": "src.main.org.apache.commons.exec.launcher.CommandLauncherProxy.CommandLauncherProxy",
    "src.main.org.apache.commons.exec.launcher.Java13CommandLauncher": "src.main.org.apache.commons.exec.launcher.Java13CommandLauncher.Java13CommandLauncher",
    "src.main.org.apache.commons.exec.launcher.OS2CommandLauncher": "src.main.org.apache.commons.exec.launcher.OS2CommandLauncher.OS2CommandLauncher",
    "src.main.org.apache.commons.exec.launcher.VmsCommandLauncher": "src.main.org.apache.commons.exec.launcher.VmsCommandLauncher.VmsCommandLauncher",
    "src.main.org.apache.commons.exec.launcher.WinNTCommandLauncher": "src.main.org.apache.commons.exec.launcher.WinNTCommandLauncher.WinNTCommandLauncher",
    "src.main.org.apache.commons.exec.util.DebugUtils": "src.main.org.apache.commons.exec.util.DebugUtils.DebugUtils",
    "src.main.org.apache.commons.exec.util.MapUtils": "src.main.org.apache.commons.exec.util.MapUtils.MapUtils",
    "src.main.org.apache.commons.exec.util.StringUtils": "src.main.org.apache.commons.exec.util.StringUtils.StringUtils",
    "src.main.org.apache.commons.exec.CommandLine": "src.main.org.apache.commons.exec.CommandLine.CommandLine",
    "src.main.org.apache.commons.exec.CommandLine$Argument": "src.main.org.apache.commons.exec.CommandLine.Argument",
    "src.main.org.apache.commons.exec.DaemonExecutor": "src.main.org.apache.commons.exec.DaemonExecutor.DaemonExecutor",
    "src.main.org.apache.commons.exec.DaemonExecutor$Builder": "src.main.org.apache.commons.exec.DaemonExecutor.Builder",
    "src.main.org.apache.commons.exec.DefaultExecuteResultHandler": "src.main.org.apache.commons.exec.DefaultExecuteResultHandler.DefaultExecuteResultHandler",
    "src.main.org.apache.commons.exec.DefaultExecutor": "src.main.org.apache.commons.exec.DefaultExecutor.DefaultExecutor",
    "src.main.org.apache.commons.exec.DefaultExecutor$Builder": "src.main.org.apache.commons.exec.DefaultExecutor.Builder",
    "src.main.org.apache.commons.exec.ExecuteException": "src.main.org.apache.commons.exec.ExecuteException.ExecuteException",
    "src.main.org.apache.commons.exec.ExecuteResultHandler": "src.main.org.apache.commons.exec.ExecuteResultHandler.ExecuteResultHandler",
    "src.main.org.apache.commons.exec.ExecuteStreamHandler": "src.main.org.apache.commons.exec.ExecuteStreamHandler.ExecuteStreamHandler",
    "src.main.org.apache.commons.exec.ExecuteWatchdog": "src.main.org.apache.commons.exec.ExecuteWatchdog.ExecuteWatchdog",
    "src.main.org.apache.commons.exec.ExecuteWatchdog$Builder": "src.main.org.apache.commons.exec.ExecuteWatchdog.Builder",
    "src.main.org.apache.commons.exec.Executor": "src.main.org.apache.commons.exec.Executor.Executor",
    "src.main.org.apache.commons.exec.InputStreamPumper": "src.main.org.apache.commons.exec.InputStreamPumper.InputStreamPumper",
    "src.main.org.apache.commons.exec.LogOutputStream": "src.main.org.apache.commons.exec.LogOutputStream.LogOutputStream",
    "src.main.org.apache.commons.exec.LogOutputStream$ByteArrayOutputStreamX": "src.main.org.apache.commons.exec.LogOutputStream.ByteArrayOutputStreamX",
    "src.main.org.apache.commons.exec.OS": "src.main.org.apache.commons.exec.OS.OS",
    "src.main.org.apache.commons.exec.ProcessDestroyer": "src.main.org.apache.commons.exec.ProcessDestroyer.ProcessDestroyer",
    "src.main.org.apache.commons.exec.PumpStreamHandler": "src.main.org.apache.commons.exec.PumpStreamHandler.PumpStreamHandler",
    "src.main.org.apache.commons.exec.ShutdownHookProcessDestroyer": "src.main.org.apache.commons.exec.ShutdownHookProcessDestroyer.ShutdownHookProcessDestroyer",
    "src.main.org.apache.commons.exec.ShutdownHookProcessDestroyer$ProcessDestroyerThread": "src.main.org.apache.commons.exec.ShutdownHookProcessDestroyer.ProcessDestroyerThread",
    "src.main.org.apache.commons.exec.StreamPumper": "src.main.org.apache.commons.exec.StreamPumper.StreamPumper",
    "src.main.org.apache.commons.exec.ThreadUtil": "src.main.org.apache.commons.exec.ThreadUtil.ThreadUtil",
    "src.main.org.apache.commons.exec.TimeoutObserver": "src.main.org.apache.commons.exec.TimeoutObserver.TimeoutObserver",
    "src.main.org.apache.commons.exec.Watchdog": "src.main.org.apache.commons.exec.Watchdog.Watchdog",
    "src.main.org.apache.commons.exec.Watchdog$Builder": "src.main.org.apache.commons.exec.Watchdog.Builder",
    "src.test.org.apache.commons.exec.TestUtil": "src.test.org.apache.commons.exec.TestUtil.TestUtil",
    "src.test.org.apache.commons.exec.TutorialTest$PrintResultHandler": "src.test.org.apache.commons.exec.TutorialTest.PrintResultHandler",

    "src.main.org.fusesource.jansi.internal.CLibrary": "src.main.org.fusesource.jansi.internal.CLibrary.CLibrary",
    "src.main.org.fusesource.jansi.internal.CLibrary$WinSize": "src.main.org.fusesource.jansi.internal.CLibrary.WinSize",
    "src.main.org.fusesource.jansi.internal.CLibrary$Termios": "src.main.org.fusesource.jansi.internal.CLibrary.Termios",
    "src.main.org.fusesource.jansi.internal.JansiLoader": "src.main.org.fusesource.jansi.internal.JansiLoader.JansiLoader",
    "src.main.org.fusesource.jansi.internal.Kernel32": "src.main.org.fusesource.jansi.internal.Kernel32.Kernel32",
    "src.main.org.fusesource.jansi.internal.Kernel32$SMALL_RECT": "src.main.org.fusesource.jansi.internal.Kernel32.SMALL_RECT",
    "src.main.org.fusesource.jansi.internal.Kernel32$COORD": "src.main.org.fusesource.jansi.internal.Kernel32.COORD",
    "src.main.org.fusesource.jansi.internal.Kernel32$CONSOLE_SCREEN_BUFFER_INFO": "src.main.org.fusesource.jansi.internal.Kernel32.CONSOLE_SCREEN_BUFFER_INFO",
    "src.main.org.fusesource.jansi.internal.Kernel32$CHAR_INFO": "src.main.org.fusesource.jansi.internal.Kernel32.CHAR_INFO",
    "src.main.org.fusesource.jansi.internal.Kernel32$KEY_EVENT_RECORD": "src.main.org.fusesource.jansi.internal.Kernel32.KEY_EVENT_RECORD",
    "src.main.org.fusesource.jansi.internal.Kernel32$MOUSE_EVENT_RECORD": "src.main.org.fusesource.jansi.internal.Kernel32.MOUSE_EVENT_RECORD",
    "src.main.org.fusesource.jansi.internal.Kernel32$WINDOW_BUFFER_SIZE_RECORD": "src.main.org.fusesource.jansi.internal.Kernel32.WINDOW_BUFFER_SIZE_RECORD",
    "src.main.org.fusesource.jansi.internal.Kernel32$FOCUS_EVENT_RECORD": "src.main.org.fusesource.jansi.internal.Kernel32.FOCUS_EVENT_RECORD",
    "src.main.org.fusesource.jansi.internal.Kernel32$MENU_EVENT_RECORD": "src.main.org.fusesource.jansi.internal.Kernel32.MENU_EVENT_RECORD",
    "src.main.org.fusesource.jansi.internal.Kernel32$INPUT_RECORD": "src.main.org.fusesource.jansi.internal.Kernel32.INPUT_RECORD",
    "src.main.org.fusesource.jansi.internal.MingwSupport": "src.main.org.fusesource.jansi.internal.MingwSupport.MingwSupport",
    "src.main.org.fusesource.jansi.internal.OSInfo": "src.main.org.fusesource.jansi.internal.OSInfo.OSInfo",
    "src.main.org.fusesource.jansi.io.AnsiOutputStream": "src.main.org.fusesource.jansi.io.AnsiOutputStream.AnsiOutputStream",
    "src.main.org.fusesource.jansi.io.AnsiOutputStream$IoRunnable": "src.main.org.fusesource.jansi.io.AnsiOutputStream.IoRunnable",
    "src.main.org.fusesource.jansi.io.AnsiOutputStream$WidthSupplier": "src.main.org.fusesource.jansi.io.AnsiOutputStream.WidthSupplier",
    "src.main.org.fusesource.jansi.io.AnsiOutputStream$ZeroWidthSupplier": "src.main.org.fusesource.jansi.io.AnsiOutputStream.ZeroWidthSupplier",
    "src.main.org.fusesource.jansi.io.AnsiProcessor": "src.main.org.fusesource.jansi.io.AnsiProcessor.AnsiProcessor",
    "src.main.org.fusesource.jansi.io.Colors": "src.main.org.fusesource.jansi.io.Colors.Colors",
    "src.main.org.fusesource.jansi.io.ColorsAnsiProcessor": "src.main.org.fusesource.jansi.io.ColorsAnsiProcessor.ColorsAnsiProcessor",
    "src.main.org.fusesource.jansi.io.FastBufferedOutputStream": "src.main.org.fusesource.jansi.io.FastBufferedOutputStream.FastBufferedOutputStream",
    "src.main.org.fusesource.jansi.io.WindowsAnsiProcessor": "src.main.org.fusesource.jansi.io.WindowsAnsiProcessor.WindowsAnsiProcessor",
    "src.main.org.fusesource.jansi.Ansi": "src.main.org.fusesource.jansi.io.Ansi.Ansi",
    "src.main.org.fusesource.jansi.Ansi$Consumer": "src.main.org.fusesource.jansi.io.Ansi.Consumer",
    "src.main.org.fusesource.jansi.AnsiColors": "src.main.org.fusesource.jansi.io.AnsiColors.AnsiColors",
    "src.main.org.fusesource.jansi.AnsiConsole": "src.main.org.fusesource.jansi.io.AnsiConsole.AnsiConsole",
    "src.main.org.fusesource.jansi.AnsiMain": "src.main.org.fusesource.jansi.io.AnsiMain.AnsiMain",
    "src.main.org.fusesource.jansi.AnsiMode": "src.main.org.fusesource.jansi.io.AnsiMode.AnsiMode",
    "src.main.org.fusesource.jansi.AnsiPrintStream": "src.main.org.fusesource.jansi.io.AnsiPrintStream.AnsiPrintStream",
    "src.main.org.fusesource.jansi.AnsiRenderer": "src.main.org.fusesource.jansi.io.AnsiRenderer.AnsiRenderer",
    "src.main.org.fusesource.jansi.AnsiType": "src.main.org.fusesource.jansi.io.AnsiType.AnsiType",
    "src.main.org.fusesource.jansi.WindowsSupport": "src.main.org.fusesource.jansi.io.WindowsSupport.WindowsSupport",

    

    
    
    
} 

def convert_to_python(json_obj, force_new_object=False):
    """
    Recursively convert the JSON object from Java's customToString()
    to the corresponding Python objects based on the type_map.
    Java memory address used to avoid duplicate object creation when pointer aliases
    Flag `force_new_object` only set to `True` when creating dummy objects for equivalence check.
    """
    global reference_dict
    java_type = json_obj.get("type")
    if not java_type:
        return None

    if "value" in json_obj:
        if json_obj.get("value") is None:
            return None

    python_type = type_map.get(java_type, java_type)

    if python_type == 'str':
        return json_obj.get("value", None)
    elif python_type == 'int':
        int_val = json_obj.get("value", None)
        if int_val is None:
            return None
        return int(int_val)
    elif python_type == 'float' or python_type == 'numbers.Number':
        float_val = json_obj.get("value", None)
        if float_val is None:
            return None
        return float(float_val)
    elif python_type == 'bool':
        bool_val = json_obj.get("value", None)
        if bool_val == "true":
            return True
        elif bool_val == "false":
            return False
        else:
            return None
    elif python_type == 'tuple':
        collection_elements = json_obj.get("collection_elements", [])
        tuple_object = tuple([convert_to_python(elem, force_new_object=force_new_object) for elem in collection_elements])
        memory_address = json_obj.get("memory_address")
        if force_new_object or not memory_address:
            return tuple_object
        if memory_address in reference_dict:
            return reference_dict[memory_address]
        else:
            reference_dict[memory_address] = tuple_object
            return reference_dict[memory_address]
    elif python_type == 'list' or python_type.endswith("[]"):
        lst = json_obj.get("collection_elements", [])
        list_object = [convert_to_python(elem, force_new_object=force_new_object) for elem in lst]
        memory_address = json_obj.get("memory_address")
        if force_new_object or not memory_address:
            return list_object
        if memory_address in reference_dict:
            reference_dict[memory_address].clear()
            reference_dict[memory_address].extend(list_object)
        else:
            reference_dict[memory_address] = list_object
        return reference_dict[memory_address]
    elif python_type == 'dict_keys':
        key_set = json_obj.get("collection_elements", None)
        keys = [convert_to_python(elem, force_new_object=force_new_object) for elem in key_set]
        dummy_dict_keys = {keys[i]: i for i in range(len(keys))}.keys()
        memory_address = json_obj.get("memory_address")
        if force_new_object or not memory_address:
            return dummy_dict_keys
        reference_dict[memory_address] = dummy_dict_keys
        return reference_dict[memory_address]
    elif python_type == 'dict_values':
        lst = json_obj.get("collection_elements", None)
        values = [convert_to_python(elem, force_new_object=force_new_object) for elem in lst]
        dummy_dict_values = {i: values[i] for i in range(len(values))}.values()
        memory_address = json_obj.get("memory_address")
        if force_new_object or not memory_address:
            return dummy_dict_values
        reference_dict[memory_address] = dummy_dict_values
        return reference_dict[memory_address]
    elif python_type == 'set':
        elements = json_obj.get("collection_elements", set())
        set_object = set()
        for element in elements:
            set_object.add(convert_to_python(element, force_new_object=force_new_object))
        memory_address = json_obj.get("memory_address")
        if force_new_object or not memory_address:
            return set_object
        if memory_address in reference_dict:
            reference_dict[memory_address].clear()
            reference_dict[memory_address].update(set_object)
        else:
            reference_dict[memory_address] = set_object
        return reference_dict[memory_address]
    elif python_type == 'dict':
        keys = json_obj.get("keys", [])
        values = json_obj.get("values", [])
        dict_object = {convert_to_python(key, force_new_object=force_new_object): convert_to_python(value, force_new_object=force_new_object) for key, value in zip(keys, values)}
        memory_address = json_obj.get("memory_address")
        if force_new_object or not memory_address:
            return dict_object
        if memory_address in reference_dict:
            reference_dict[memory_address].clear()
            reference_dict[memory_address].update(dict_object)
        else:
            reference_dict[memory_address] = dict_object
        return reference_dict[memory_address]
    elif python_type == 'Exception':
        exception_cls = getattr(builtins, type_map.get(json_obj.get("throwable_type", "java.lang.Throwable"), "Exception"))
        return exception_cls(json_obj.get("message", None))
    elif python_type == 'PeekableIterator':
        peekable_iterator_object = PeekableIterator([])
        collection = json_obj.get("collection_details", {}).get("collection_elements", None)
        if collection is None:
            keys = json_obj.get("collection_details", {}).get("keys", None)
            values = json_obj.get("collection_details", {}).get("values", None)
            if keys is None or values is None:
                return peekable_iterator_object
            else:
                peekable_iterator_object = PeekableIterator({
                    convert_to_python(key, force_new_object=force_new_object): convert_to_python(value, force_new_object=force_new_object) for key, value in zip(keys, values)
                })
        else:
            peekable_iterator_object = PeekableIterator([convert_to_python(elem, force_new_object=force_new_object) for elem in collection])
        memory_address = json_obj.get("memory_address")
        if force_new_object or not memory_address:
            return peekable_iterator_object
        if memory_address in reference_dict:
            reference_dict[memory_address].__dict__.clear()
            reference_dict[memory_address].__dict__.update(peekable_iterator_object.__dict__)
        else:
            reference_dict[memory_address] = peekable_iterator_object
        return reference_dict[memory_address]
    elif python_type == "urllib.parse.ParseResult":
        return urlparse(json_obj.get("value", ""))
    elif python_type == "io.BytesIO":
        byte_array_json = json_obj.get("byte_array", None)
        if byte_array_json is None:
            byte_array_json = json_obj.get("sink_details", None)
            if byte_array_json is None:
                byte_array = []
            else:
                byte_array = convert_to_python(json_obj.get("sink_details").get("byte_array"))
        else:
            byte_array = convert_to_python(byte_array_json)
        byte_buffer = bytes([x & 0xFF for x in byte_array])
        if java_type == "java.io.ByteArrayInputStream":
            bytes_io_object = BytesIO(byte_buffer)
            bytes_io_object.seek(int(json_obj.get("position", 0)))
        else:
            size = int(json_obj.get("size", 0))
            bytes_io_object = BytesIO(byte_buffer[:size])
            if "position" in json_obj:
                bytes_io_object.seek(int(json_obj.get("position", 0)))
            else:
                bytes_io_object.seek(size)
            
        memory_address = json_obj.get("memory_address")
        if force_new_object or not memory_address:
            return bytes_io_object
        if memory_address in reference_dict:
            reference_dict[memory_address].seek(0)
            reference_dict[memory_address].truncate(0)
            reference_dict[memory_address].write(bytes_io_object.getvalue())
            reference_dict[memory_address].seek(int(json_obj.get("position", 0)))
        else:
            reference_dict[memory_address] = bytes_io_object
        return reference_dict[memory_address]
    elif python_type == "io.StringIO":
        if json_obj.get("special_note", None) is not None:
            if json_obj.get("special_note") == "System.out":
                return sys.stdout
            elif json_obj.get("special_note") == "System.err":
                return sys.stderr
            elif json_obj.get("special_note") == "byte_stream":
                return convert_to_python(json_obj.get("byte_stream"))
        content = json_obj.get("content", None)
        position = int(json_obj.get("position", 0))
        if content is None:
            content = json_obj.get("value", "")
            position = len(content)
        string_io_object = StringIO()
        string_io_object.write(content)
        if "position" in json_obj:
            string_io_object.seek(position)
        memory_address = json_obj.get("memory_address")
        if force_new_object or not memory_address:
            return string_io_object
        if memory_address in reference_dict:
            reference_dict[memory_address].seek(0)
            reference_dict[memory_address].truncate(0)
            reference_dict[memory_address].write(string_io_object.getvalue())
            if "position" in json_obj:
                reference_dict[memory_address].seek(int(json_obj.get("position")))
        else:
            reference_dict[memory_address] = string_io_object
        return reference_dict[memory_address]
    elif python_type == "io.BufferedReader":
        if json_obj.get("stream_type", None) is not None:
            if json_obj.get("stream_type") == "byte_stream":
                byte_stream = convert_to_python(json_obj.get("stream_details"))
                content_bytes = byte_stream.getvalue()
                position = byte_stream.tell()
            elif json_obj.get("stream_type") == "file_stream":
                obj = convert_to_python(json_obj.get("stream_details"))
                return BufferedReader(obj.buffer.raw)
            else:
                return None
        elif json_obj.get("special_note", None) is not None:
            if json_obj.get("special_note") == "System.out":
                return TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
            elif json_obj.get("special_note") == "System.err":
                return TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
            elif json_obj.get("special_note") == "byte_stream":
                byte_stream = convert_to_python(json_obj.get("byte_stream"))
                content_bytes = byte_stream.getvalue()
                position = byte_stream.tell()
        else:
            content = json_obj.get("content", "")
            position = int(json_obj.get("position", 0))
            content_bytes = content.encode("utf-8") 
            byte_stream = BytesIO(content_bytes)
            byte_stream.seek(position)
        br = BufferedReader(byte_stream)
        br.seek(0)
        memory_address = json_obj.get("memory_address")
        if force_new_object or not memory_address:
            return br
        if memory_address in reference_dict:
            underlying = reference_dict[memory_address].raw
            underlying.seek(0)
            underlying.truncate(0)
            underlying.write(content_bytes)
            underlying.seek(position)
        else:
            reference_dict[memory_address] = br
        return reference_dict[memory_address]
    elif python_type == "io.BufferedWriter":
        if json_obj.get("stream_type") == "byte_stream":
            byte_stream = convert_to_python(json_obj.get("stream_details"))
            content_bytes = obj.getvalue()
            position = obj.tell()
            bw = BufferedWriter(byte_stream)
            memory_address = json_obj.get("memory_address")
            bw.seek(0)
            if force_new_object or not memory_address:    
                return bw
            if memory_address in reference_dict:
                underlying = reference_dict[memory_address].raw
                underlying.seek(0)
                underlying.truncate(0)
                underlying.write(content_bytes)
                underlying.seek(position)
            else:
                reference_dict[memory_address] = bw
            return reference_dict[memory_address]
        elif json_obj.get("stream_type") == "file_stream":
            obj = convert_to_python(json_obj.get("stream_details"))
            return BufferedWriter(obj.buffer.raw)
        else:
            return None
    elif python_type == "src.main.org.apache.commons.fileupload.util.LimitedInputStream.LimitedInputStream"\
        or python_type == "src.main.org.apache.commons.codec.binary.BaseNCodecInputStream.BaseNCodecInputStream"\
        or python_type == "src.main.org.apache.commons.codec.binary.Base16InputStream.Base16InputStream"\
        or python_type == "src.main.org.apache.commons.codec.binary.Base32InputStream.Base32InputStream"\
        or python_type == "src.main.org.apache.commons.codec.binary.Base64InputStream.Base64InputStream"\
        or python_type == "src.main.org.apache.commons.codec.binary.BaseNCodecOutputStream.BaseNCodecOutputStream"\
        or python_type == "src.main.org.apache.commons.codec.binary.Base16OutputStream.Base16OutputStream"\
        or python_type == "src.main.org.apache.commons.codec.binary.Base32OutputStream.Base32OutputStream"\
        or python_type == "src.main.org.apache.commons.codec.binary.Base64OutputStream.Base64OutputStream":
        underlying = None
        if json_obj.get("stream_type", None) is not None:
            if json_obj.get("stream_type") == "byte_stream":
                underlying = convert_to_python(json_obj.get("stream_details"))
            elif json_obj.get("stream_type") == "file_stream":
                underlying = convert_to_python(json_obj.get("stream_details")).buffer.raw
            else:
                underlying = BytesIO()
        else:
            underlying = BytesIO()
        clazz = globals().get(python_type)
        obj = clazz.__new__(clazz)
        BufferedReader.__init__(obj, underlying)
        className = obj.__class__.__name__
        instance_fields = json_obj.get("instance_fields", {})
        for field_name, field_details in instance_fields.items():
            if "modifier" in field_details:
                if field_details.get("modifier") == "private":
                    setattr(obj, "_" + className + "__" + field_name, convert_to_python(field_details))
                elif field_details.get("modifier") == "protected":
                    setattr(obj, "_" + field_name, convert_to_python(field_details))
                else:
                    setattr(obj, field_name, convert_to_python(field_details))
            else:
                setattr(obj, field_name, convert_to_python(field_details))
        return obj
    elif python_type == "src.main.org.apache.commons.csv.ExtendedBufferedReader.ExtendedBufferedReader":
        content = json_obj.get("content", "")
        content_bytes = content.encode("utf-8")
        byte_stream = BytesIO(content_bytes)
        extendedBufferedReader_clazz = globals().get(python_type)
        extendedBufferedReader_obj = extendedBufferedReader_clazz.__new__(extendedBufferedReader_clazz)
        BufferedReader.__init__(extendedBufferedReader_obj, byte_stream)
        className = extendedBufferedReader_obj.__class__.__name__
        instance_fields = json_obj.get("instance_fields", {})
        for field_name, field_details in instance_fields.items():
            if "modifier" in field_details:
                if field_details.get("modifier") == "private":
                    setattr(extendedBufferedReader_obj, "_" + className + "__" + field_name, convert_to_python(field_details))
                elif field_details.get("modifier") == "protected":
                    setattr(extendedBufferedReader_obj, "_" + field_name, convert_to_python(field_details))
                else:
                    setattr(extendedBufferedReader_obj, field_name, convert_to_python(field_details))
            else:
                setattr(extendedBufferedReader_obj, field_name, convert_to_python(field_details))
        extendedBufferedReader_obj.seek(extendedBufferedReader_obj._ExtendedBufferedReader__position)
        return extendedBufferedReader_obj   
    elif python_type == "io.FileIO":
        file_path = json_obj.get("file_path")
        position = json_obj.get("position")
        file_size = json_obj.get("file_size")
        file_io_object = None
        try:
            file_io_object = open(file_path, 'r')
            actual_size = file_io_object.seek(0, 2)  # Move to the end of the file to get its size
            if actual_size != file_size:
                print(f"Warning: File size mismatch. Expected {file_size}, but got {actual_size}.")
            file_io_object.seek(position)  # Position the pointer at the given `position`
        except FileNotFoundError:
            print(f"Error: The file at {file_path} does not exist.")
        except Exception as e:
            print(f"Error: {str(e)}")
        memory_address = json_obj.get("memory_address")
        if force_new_object or not memory_address:
            return file_io_object
        if memory_address in reference_dict:
            reference_dict[memory_address].seek(0)
            reference_dict[memory_address].truncate(0)
            reference_dict[memory_address].write(file_io_object.buffer.getvalue().decode("utf-8"))
            reference_dict[memory_address].seek(int(json_obj.get("position")))
        else:
            reference_dict[memory_address] = file_io_object
        return reference_dict[memory_address]
    elif python_type == 'io.TextIOWrapper':
        encoding = json_obj.get("encoding", "utf-8")
        special_note = json_obj.get("special_note", "")
        textIOWrapper_obj = None
        if special_note == "System.in":
            textIOWrapper_obj = TextIOWrapper(sys.stdin.buffer, encoding=encoding)
        elif special_note == "byte_stream":
            textIOWrapper_obj = TextIOWrapper(convert_to_python(json_obj.get("byte_stream")), encoding=encoding)
        elif special_note == "file_stream":
            textIOWrapper_obj = convert_to_python(json_obj.get("file_stream"))
        memory_address = json_obj.get("memory_address")
        if force_new_object or not memory_address:
            return textIOWrapper_obj
        if memory_address in reference_dict:
            existing_wrapper = reference_dict[memory_address]
            try:
                if hasattr(textIOWrapper_obj.buffer, 'getvalue'):
                    content_bytes = textIOWrapper_obj.buffer.getvalue()
                    existing_wrapper.buffer.seek(0)
                    existing_wrapper.buffer.truncate(0)
                    existing_wrapper.buffer.write(content_bytes)
                    existing_wrapper.buffer.seek(0)
                else:
                    reference_dict[memory_address].seek(0)
                    reference_dict[memory_address].truncate(0)
                    reference_dict[memory_address].write(textIOWrapper_obj.buffer.getvalue().decode("utf-8"))
                    reference_dict[memory_address].seek(int(json_obj.get("file_stream").get("position")))
            except Exception:
                reference_dict[memory_address] = textIOWrapper_obj
        else:
            reference_dict[memory_address] = textIOWrapper_obj
        return reference_dict[memory_address]
    elif python_type == 'type':
        java_clazz_name = json_obj.get("value", "null")
        if java_clazz_name.startswith("[L"):
            return list
        python_clazz_name = type_map.get(java_clazz_name, java_clazz_name)
        if python_clazz_name == 'None':
            return None
        try:
            clazz = getattr(builtins, python_clazz_name)
            return clazz
        except AttributeError:
            try:
                clazz = globals().get(python_clazz_name)
                if clazz is None:
                    module_name, class_name = python_clazz_name.rsplit('.', 1)
                    module = importlib.import_module(module_name)
                    clazz = getattr(module, class_name)
                return clazz
            except (ValueError, ImportError, AttributeError):
                clazz = globals().get(type_map.get("src.main." + java_clazz_name, None))
                if not clazz:
                    clazz = globals().get(type_map.get("src.test." + java_clazz_name, None))
                if not clazz:
                    return None
                else:
                    return clazz
    elif python_type == 'pathlib.Path':
        path_str = json_obj.get("value", None)
        return Path(path_str)
    elif python_type == 'datetime.datetime':
        datetime_object = datetime(1970, 1, 1)
        if "timestamp" in json_obj:
            ts = json_obj.get("timestamp")
            tz = timezone.utc if "timezone" not in json_obj else timezone(json_obj.get("timezone"))
            datetime_object = datetime.fromtimestamp(ts, tz)
        elif "instant" in json_obj:
            datetime_object = datetime.fromisoformat(json_obj.get("instant"))
        memory_address = json_obj.get("memory_address")
        if force_new_object or not memory_address:
            return datetime_object
        if memory_address in reference_dict:
            delta = datetime_object - reference_dict[memory_address]
            reference_dict[memory_address] = reference_dict[memory_address] + delta
        else:
            reference_dict[memory_address] = datetime_object
        return reference_dict[memory_address]
    elif python_type == 'datetime.timedelta':
        td = timedelta(0)
        seconds = json_obj.get("seconds", 0)
        nanos = json_obj.get("nanos", 0)
        total_microseconds = seconds * 1_000_000 + nanos / 1_000
        days, rem = divmod(total_microseconds, 86_400_000_000)
        seconds, rem = divmod(rem, 1_000_000)
        microseconds = rem
        if "nanos" in json_obj:
            td = timedelta(days=days, seconds=seconds, microseconds=microseconds)
        memory_address = json_obj.get("memory_address")
        if force_new_object or not memory_address:
            return td
        if memory_address in reference_dict:
            delta = td - reference_dict[memory_address]
            reference_dict[memory_address] += delta
        else:
            reference_dict[memory_address] = td
        return reference_dict[memory_address]
    elif python_type == 'threading.Thread':
        return Thread(target=None, name=None, args=(), kwargs=None, daemon=False)
    elif python_type == 'typing.Callable':
        callable_instance_str = json_obj.get("value", None)
        callable_obj = None
        if "@" in callable_instance_str:
            callable_type = callable_instance_str.split("@")[0]
        callable_class = globals().get(type_map.get('src.main.' + callable_type), None)
        if callable_class is not None:
            callable_obj = object.__new__(callable_class)
        memory_address = json_obj.get("memory_address")
        if force_new_object or not memory_address:
            return callable_obj
        if memory_address in reference_dict:
            reference_dict[memory_address].__call__ = callable_obj.__call__
        else:
            reference_dict[memory_address] = callable_obj
        return reference_dict[memory_address]
    elif "_AnonymousClass_" in python_type:
        return globals()[python_type]()
    elif python_type == 'None':
        return None
    else:
        return create_python_object(python_type, json_obj, force_new_object=force_new_object)


def extract_balanced_brackets(s: str, start: int):
    """
    From a starting index, return the content of the next balanced bracket section.
    """
    stack = []
    i = start
    in_string = False
    escape = False

    while i < len(s):
        c = s[i]
        if escape:
            escape = False
        elif c == "\\":
            escape = True
        elif c in "\"'":
            in_string = not in_string
        elif not in_string:
            if c == "[":
                stack.append("[")
            elif c == "]":
                if not stack:
                    return s[start:i].strip(), i
                stack.pop()
        i += 1
    return None, None


def extract_named_sections(s: str) -> dict:
    """
    Extracts sections like [ short {...} ] or [ long {...} ] into a dict
    with keys "short", "long", etc.
    """
    sections = {}
    pattern = re.compile(r"\[\s*(\w+)\s+")
    pos = 0
    while True:
        match = pattern.search(s, pos)
        if not match:
            break

        name = match.group(1)
        start = match.end()
        content, end = extract_balanced_brackets(s, start)
        if content is None:
            raise ValueError(f"Could not find balanced content for section '{name}' starting at position {start}")

        norm_blob = normalize_struct(content)
        try:
            parsed = ast.literal_eval(norm_blob)
        except Exception as e:
            raise ValueError(f"Failed to parse section '{name}': {e}\nOriginal:\n{content}")
        sections[name] = parsed
        pos = end + 1  # move to next match
    return sections

def normalize_struct(s: str) -> str:
    """
    Replace: K
    Java object refs -> <_anyobject_> placeholder
    Java class refs -> <class> placeholder
    `[ option: ... :: ... :: ... ]` (`Option` class specific structure) -> <object> placeholder
    Normalize key: value and key=value to 'key': value ). (Java HashMap <--> Python Dict)
    """
    s = re.sub(r'<[^>]+?object at 0x[0-9a-fA-F]+>', '"<_anyobject_>"', s)
    s = re.sub(r"\[ option:.*?::.*?::.*?\]", '"<_anyobject_>"', s)
    s = re.sub(r'class\s+[\w.$]+', '"<class>"', s)
    s = re.sub(r"<class\s+'[\w.]+'?>", '"<class>"', s)
    s = re.sub(r"(?<!['\"])(\b\w+)\s*[:=]\s*", r"'\1': ", s)
    return s


def logically_equal(java_str: str, py_str: str) -> bool:
    """ Check if two strings are equal according to CLI specifics """
    try:
        if java_str.strip().startswith("[ option:") and py_str.strip().startswith("[ option:"):
            norm_java = normalize_struct(java_str).strip()
            norm_py = normalize_struct(py_str).strip()
            return norm_java == norm_py
        java_sections = extract_named_sections(java_str)
        py_sections = extract_named_sections(py_str)
        if not java_sections or not py_sections:
            return False
        return java_sections == py_sections
    except Exception as e:
        print(f"Error during comparison: {e}")
        return False

def is_sublist(a, b):
    """Return True if list a is a sublist of list b."""
    if not a:
        return True
    len_a = len(a)
    return any(b[i:i+len_a] == a for i in range(len(b) - len_a + 1))

def recursive_equal(obj1, obj2):
    """
    Recursively checks equality of two Python objects by comparing their attributes and values.
    """
    if obj1 is obj2:
        return True
    if isinstance(obj1, Enum) and isinstance(obj2, Enum):
        return obj1._name_ == obj2._name_ and recursive_equal(obj1._value_, obj2._value_)
    if isinstance(obj1, Exception) and isinstance(obj2, Exception):
        if issubclass(type(obj1), type(obj2)) or issubclass(type(obj2), type(obj1)):
            return True # Skip strict message equivalence check
        else:
            return False
    if isinstance(obj1, Thread) and isinstance(obj2, Thread):
        return True
    if isinstance(obj1, int) and isinstance(obj2, int) and obj1 != obj2:
        for obj in reference_dict.values():
            try:
                obj_hashcode = hash(obj)
            except TypeError:
                if hasattr(obj, '__dict__'):
                    for field1 in obj.__dict__:
                        try:
                            tuple_with_first_None_hashcode = hash((None, getattr(obj, field1)))
                        except TypeError:
                            pass
                        if tuple_with_first_None_hashcode == obj1:
                            return True
                        try:
                            tuple_with_second_None_hashcode = hash((getattr(obj, field1), None))
                        except TypeError:
                            pass
                        if tuple_with_second_None_hashcode == obj1:
                            return True
                        for field2 in obj.__dict__:
                            try:
                                field1_hashcode = hash(getattr(obj, field1))
                                field2_hashcode = hash(getattr(obj, field2))
                                tuple_hashcode = hash((getattr(obj, field1), getattr(obj, field2)))
                            except TypeError:
                                continue
                            if field1_hashcode == obj1 or field2_hashcode == obj1 or tuple_hashcode == obj1:
                                return True
                continue
            if obj_hashcode == obj1:
                return True
        return False
    if isinstance(obj1, timedelta) and isinstance(obj2, timedelta):
        TOLERANCE_SECONDS = 1e-6  # allow 1 microsecond difference (avoid numerical issues)
        if abs(obj1.total_seconds() - obj2.total_seconds()) < TOLERANCE_SECONDS:
            return True
        else:
            return False
    if isinstance(obj1, str) and isinstance(obj2, str) and not obj1 == obj2:
        return logically_equal(obj1, obj2)
    if not isinstance(obj1, Iterator) and type(obj1) != type(obj2):
        return False
    if isinstance(obj1, (BytesIO, StringIO)):
        return obj1.getvalue() == obj2.getvalue()
    if isinstance(obj1, dict):
        if obj1.keys() != obj2.keys():
            return False
        return all([recursive_equal(obj1[key], obj2[key]) for key in obj1])
    elif isinstance(obj1, list):
        if len(obj1) != len(obj2):
            return False
        return all(recursive_equal(item1, item2) for item1, item2 in zip(obj1, obj2))
    elif isinstance(obj1, set):
        if len(obj1) != len(obj2):
            return False
        for item1 in obj1:
            if not any(recursive_equal(item1, item2) for item2 in obj2):
                return False
        return True
    elif isinstance(obj1, urllib.parse.ParseResult):
        return recursive_equal(obj1._asdict(), obj2._asdict())
    elif isinstance(obj1, datetime):
        return obj1.timestamp() == obj2.timestamp()
    elif isinstance(obj1, tuple):
        if len(obj1) != len(obj2):
            return False
        return all(recursive_equal(item1, item2) for item1, item2 in zip(obj1, obj2))
    elif isinstance(obj1, Iterator) and isinstance(obj2, Iterator):
        try:
            obj1_list = PeekableIterator(obj1).to_list()
            obj2_list = PeekableIterator(obj2).to_list()
            if recursive_equal(obj1_list, obj2_list):
                return True
            else:
                return is_sublist(obj2_list, obj1_list)
        except ValueError as e:
            if str(e) == "I/O operation on closed file.":
                return True
            else:
                raise
    elif isinstance(obj1, type({}.values())) and isinstance(obj2, type({}.values())):
        return recursive_equal(list(obj1), list(obj2))
    elif hasattr(obj1, '__dict__') and hasattr(obj2, '__dict__'):
        obj1_dict_excluding_transient = {k: v for k, v in obj1.__dict__.items() if k in obj2.__dict__}
        return recursive_equal(obj1_dict_excluding_transient, obj2.__dict__)
    return obj1 == obj2


def get_parent_classes(clazz):
    """
    Get a list of all parent classes, excluding 'object'
    """
    return [base.__name__ for base in clazz.__bases__ if base is not object]

def set_object_instance_fields(obj, json_obj):
    """
    Update the instance fields of an object.
    Use the same instance if obj and json_obj is the same pointer(reference)
    """
    if isinstance(obj, dict) or isinstance(obj, list) or isinstance(obj, set):
        obj.clear()
        converted_json_obj = convert_to_python(json_obj)
        if not converted_json_obj is obj:
            obj.extend(converted_json_obj)
    elif isinstance(obj, BytesIO) or isinstance(obj, StringIO):
        converted_json_obj = convert_to_python(json_obj)
        obj.seek(0)
        obj.truncate(0)
        converted_json_obj = convert_to_python(json_obj)
        if not converted_json_obj is obj:
            obj.write(converted_json_obj.getvalue())
            obj.seek(converted_json_obj.tell())
    elif "PeekableIterator" == type(obj).__name__:
        other = convert_to_python(json_obj)
        obj.iterable = other
        obj.iterator = other
        obj.peeked = None
        obj.history = []
        obj.index = -1
    else:
        className = obj.__class__.__name__
        instance_fields = json_obj.get("instance_fields", {})
        for field_name, field_details in instance_fields.items():
            if "java.lang.Throwable" in field_details.get("declaring_class", ""):
                continue
            if "modifier" in field_details:
                if field_details.get("modifier") == "private":
                    declaring_class = field_details.get("declaring_class", None)
                    if declaring_class is not None:
                        setattr(obj, "_" + type_map.get(declaring_class, declaring_class).split(".")[-1] + "__" + field_name, convert_to_python(field_details))
                    else:
                        setattr(obj, "_" + className + "__" + field_name, convert_to_python(field_details))
                elif field_details.get("modifier") == "protected":
                    setattr(obj, "_" + field_name, convert_to_python(field_details))
                else:
                    setattr(obj, field_name, convert_to_python(field_details))
            else:
                setattr(obj, field_name, convert_to_python(field_details))

def create_python_object(python_type, json_obj, force_new_object=False):
    """
    Create a Python object from the type and its instance/static fields.
    """
    global reference_dict
    try:
        clazz = globals().get(python_type)
    except (ValueError, ImportError, AttributeError):
        raise Exception(f"Could not find Python class for type: {python_type}")
    if issubclass(clazz, BaseException):  # Ensure safe instantiation of exceptions
        obj = Exception.__new__(clazz)
        obj.args = (json_obj.get("instance_fields", {}).get("cause", {}).get("message", ""),)
    elif issubclass(clazz, Enum):
        obj = object.__new__(clazz)
        name = json_obj.get("value").get("enum_name") if json_obj.get("value", None) is not None else json_obj.get("enum_name")
        value = convert_to_python(json_obj.get("value").get("enum_value")) if json_obj.get("value", None) is not None else convert_to_python(json_obj.get("enum_value"))
        obj._name_ = name
        obj._value_ = value
    else:
        obj = object.__new__(clazz)

    instance_fields = json_obj.get("instance_fields", {})
    if instance_fields == {}:
        if json_obj.get("value", None) is not None and json_obj.get("type", None) is not None:
            if json_obj.get("value").get("type", None) is not None:
                if json_obj.get("value").get("type") == json_obj.get("type"):
                    instance_fields = json_obj.get('value').get("instance_fields", {})
    for field_name, field_details in instance_fields.items():
        if "java.lang.Throwable" in field_details.get("declaring_class", ""):
            continue
        if "java.io." in field_details.get("declaring_class", ""):
            continue
        if "modifier" in field_details:
            if field_details.get("modifier") == "private":
                declaring_class = field_details.get("declaring_class", None)
                if declaring_class is not None:
                    setattr(obj, "_" + type_map.get(declaring_class, declaring_class).split(".")[-1] + "__" + field_name, convert_to_python(field_details))
                else:
                    setattr(obj, "_" + python_type.split(".")[-1] + "__" + field_name, convert_to_python(field_details))
            elif field_details.get("modifier") == "protected":
                setattr(obj, "_" + field_name, convert_to_python(field_details))
            else:
                setattr(obj, field_name, convert_to_python(field_details))
        else:
            setattr(obj, field_name, convert_to_python(field_details))

    static_fields = json_obj.get("static_fields", {})
    if static_fields == {}:
        if json_obj.get("value", None) is not None and json_obj.get("type", None) is not None:
            if json_obj.get("value").get("type", None) is not None:
                if json_obj.get("value").get("type") == json_obj.get("type"):
                    instance_fields = json_obj.get('value').get("static_fields", {})
    for field_name, field_details in static_fields.items():
        if "java.lang.Throwable" in field_details.get("declaring_class", ""):
            continue
        if "java.io." in field_details.get("declaring_class", ""):
            continue
        if "modifier" in field_details:
            if field_details.get("modifier") == "private":
                declaring_class = field_details.get("declaring_class", None)
                if declaring_class is not None:
                    setattr(clazz, "_" + type_map.get(declaring_class, declaring_class).split(".")[-1] + "__" + field_name, convert_to_python(field_details))
                else:
                    setattr(clazz, "_" + python_type.split(".")[-1] + "__" + field_name, convert_to_python(field_details))
            elif field_details.get("modifier") == "protected":
                setattr(clazz, "_" + field_name, convert_to_python(field_details))
            else:
                setattr(clazz, field_name, convert_to_python(field_details))
        else:
            setattr(clazz, field_name, convert_to_python(field_details))
    memory_address = json_obj.get("memory_address")
    if force_new_object or not memory_address:
        return obj
    if memory_address in reference_dict:
        reference_dict[memory_address].__dict__.clear()
        reference_dict[memory_address].__dict__.update(obj.__dict__)
    else:
        reference_dict[memory_address] = obj
    return reference_dict[memory_address]

def update_static_fields(json_data):
    """
    Update static fields for classes based on a JSON list of dictionaries.
    Each dictionary specifies a class and its fields to update.
    """
    for class_data in json_data:
        for class_name, fields in class_data.items():
            python_class_name = type_map.get(class_name)
            clazz = globals().get(python_class_name)
            if clazz is None:
                print(f"Class '{class_name}' not found in global scope.")
                continue
            for field_update in fields:
                for field_name, field_info in field_update.items():
                    field_value = convert_to_python(field_info.get("details"))
                    if "modifier" in field_info:
                        if field_info.get("modifier") == "private":
                            declaring_class = field_info.get("declaring_class", None)
                            if declaring_class is not None:
                                setattr(clazz, "_" + type_map.get(declaring_class, declaring_class).split(".")[-1] + "__" + field_name, field_value)
                            else:
                                setattr(clazz, "_" + clazz.__name__ + "__" + field_name, field_value)
                        elif field_info.get("modifier") == "protected":
                            setattr(clazz, "_" + field_name, field_value)
                        else:
                            setattr(clazz, field_name, field_value)
                    else:
                        setattr(clazz, field_name, field_value)

def side_effect_is_correct(json_data):
    """
    Check if the current static fields are consistent with recorded JSON string
    """
    for class_data in json_data:
        for class_name, fields in class_data.items():
            clazz = globals().get(type_map.get(class_name, None))
            if clazz is None:
                print(f"Class '{class_name}' not found in global scope.")
                continue
            for field_update in fields:
                for field_name, field_info in field_update.items():
                    field_value = convert_to_python(field_info.get("details"), force_new_object=True)
                    if "modifier" in field_info:
                        if field_info.get("modifier") == "private":
                            ref_obj = getattr(clazz, "_" + clazz.__name__ + "__" + field_name, None)
                        elif field_info.get("modifier") == "protected":
                            ref_obj = getattr(clazz, "_" + field_name, None)
                        else:
                            ref_obj = getattr(clazz, field_name, None)
                    else:
                        ref_obj = getattr(clazz, field_name, None)
                    if not recursive_equal(ref_obj, field_value):
                        return False
    return True